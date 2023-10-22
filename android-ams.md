# android AMS原理

> 在学习android框架原理过程中，ams的原理非常重要，无论是在面试中还是在自己开发类库过程中都会接触到。

## 1 简述

ActivityManagerService是Android最核心的服务，负责管理四大组件的启动、切换、调度等工作。由于AMS的功能和重要性，它是运行在SystemServer进程，客户端不能直接访问。但是可以通过ActivityManager类的getService方法获取IActivityManager，然后与AMS通信。

##  2 AMS启动流程

### init进程
Android系统总共分为4层，从上到下为，应用层、框架层、系统层、linux内核层。整个系统启动时，会先由各个厂商的引导程序拉起，加载一些资源，然后启动init进程，挂载分区，创建必要目录，初始化日志系统和安全策略。最后解析init.rc文件，去启动zygote进程。
### zygote进程
通过init进程拉起zygote后，
 
```
service zygote /system/bin/app_process64 -Xzygote /system/bin --zygote --start-system-server --socket-name=zygote
    class main
    priority -20
    user root                                 # 用户为root
    group root readproc reserved_disk
    socket zygote stream 660 root system
    socket usap_pool_primary stream 660 root system
    onrestart exec_background - system system -- /system/bin/vdc volume abort_fuse
    onrestart write /sys/power/state on
    onrestart restart audioserver
    onrestart restart cameraserver
    onrestart restart media
    onrestart restart media.tuner
    onrestart restart netd
    onrestart restart wificond
    task_profiles ProcessCapacityHigh MaxPerformance
    critical window=${zygote.critical_window.minute:-off} target=zygote-fatal

service zygote_secondary /system/bin/app_process32 -Xzygote /system/bin --zygote --socket-name=zygote_secondary --enable-lazy-preload
    class main
    priority -20
    user root
    group root readproc reserved_disk
    socket zygote_secondary stream 660 root system
    socket usap_pool_secondary stream 660 root system
    onrestart restart zygote
    task_profiles ProcessCapacityHigh MaxPerformance

```

会创建JavaVM，并注册JNI
通过JNI调用ZygoteInit的main函数进入Zygote的Java框架层，创建服务端Socket，预加载类和资源，并通过runSelectLoop函数等待如ActivityManagerService等的请求。
调用forkSystemServer 来启动SystemServer进程，这样系统的关键服务也会由SystemServer进程启动起来。


## SystemServer进程

```
/**
 * 进程的入口点
 */
public static void main(String[] args) {
    new SystemServer().run();
}


private void run() {
    
    ...
        
    // 启动 AMS PowerManagerService PackageManagerService 等服务
    startBootstrapServices(t);
    // 启动了BatteryService UsageStatsService WebViewUpdateService
    startCoreServices(t);
    // CameraService AlarmManagerService VrManagerService
    startOtherServices(t);    
    ...
    
}

```

Zygote启动后fork的第一个进程为SystemServer，这个进程就会去启动一系列的服务，AMS服务也是由这个进程启动。

## AMS 启动

```
private void startBootstrapServices(@NonNull TimingsTraceAndSlog t) {
    t.traceBegin("startBootstrapServices");

    // ...

    // Activity manager runs the show.
    // 创建并运行AMS
    t.traceBegin("StartActivityManager");
    // TODO: Might need to move after migration to WM.
    ActivityTaskManagerService atm = mSystemServiceManager.startService(
        ActivityTaskManagerService.Lifecycle.class).getService();
    mActivityManagerService = ActivityManagerService.Lifecycle.startService(
        mSystemServiceManager, atm);
    mActivityManagerService.setSystemServiceManager(mSystemServiceManager);
    mActivityManagerService.setInstaller(installer);
    mWindowManagerGlobalLock = atm.getGlobalLock();
    t.traceEnd();

    // ...

    t.traceEnd(); // startBootstrapServices
}

public static final class Lifecycle extends SystemService {
    private final ActivityManagerService mService;
    private static ActivityTaskManagerService sAtm;

    public Lifecycle(Context context) {
        super(context);
        mService = new ActivityManagerService(context, sAtm);
    }

    public static ActivityManagerService startService(
        SystemServiceManager ssm, ActivityTaskManagerService atm) {
        sAtm = atm;
        return ssm.startService(ActivityManagerService.Lifecycle.class).getService();
    }

    @Override
    public void onStart() {
        mService.start();
    }

    @Override
    public void onBootPhase(int phase) {
        mService.mBootPhase = phase;
        if (phase == PHASE_SYSTEM_SERVICES_READY) {
            mService.mBatteryStatsService.systemServicesReady();
            mService.mServices.systemServicesReady();
        } else if (phase == PHASE_ACTIVITY_MANAGER_READY) {
            mService.startBroadcastObservers();
        } else if (phase == PHASE_THIRD_PARTY_APPS_CAN_START) {
            mService.mPackageWatchdog.onPackagesReady();
        }
    }

    @Override
    public void onCleanupUser(int userId) {
        mService.mBatteryStatsService.onCleanupUser(userId);
    }

    public ActivityManagerService getService() {
        return mService;
    }
}

public void startService(@NonNull final SystemService service) {
    // 注册服务
    mServices.add(service);
    // 开启服务
    long time = SystemClock.elapsedRealtime();
    try {
        service.onStart();
    } catch (RuntimeException ex) {
        throw new RuntimeException("Failed to start service " + service.getClass().getName()
                                   + ": onStart threw an exception", ex);
    }
    warnIfTooLong(SystemClock.elapsedRealtime() - time, service, "onStart");
}

private void start() {
    // ...
}

```
从代码中可以看出在startBootstrapServices方法中，创建了ActivityManagerService服务对象，然后在startService方法中调用service.onStart()，也就是走Lifecycle中实现的方法，然后最终走到start()，启动服务。




## 3 AMS在启动App过程中的体现

### fock新进程
我们手机上的App都是在Launcher（就是个Actviity）中显示的，点击图标会触发onClick收到点击事件，然后走startActivitySafely方法，继续往下走，会发现就是startActivity方法往后走的调用。
```
LauncherAppsService -> startActivityAsUser
ActivityTaskManagerService -> startActivityAsUser
ActivityStarter -> execute
ActivityStarter -> startActivityUnchecked
ActivityStarter -> startActivityInner
ActivityStack -> startActivityLocked
ActivityStack -> ensureActivitiesVisible
EnsureActivitiesVisibleHelper -> process
EnsureActivitiesVisibleHelper -> setActivityVisibilityState
ActivityRecord -> makeActiveIfNeeded
ActivityStack -> resumeTopActivityUncheckedLocked
ActivityStack -> resumeTopActivityInnerLocked
ActivityTaskManagerService -> startProcessAsync
ActivityManagerService -> startProcess
ActivityManagerService -> startProcessLocked
ProcessList -> startProcessLocked (指定启动进程后，走android.app.ActivityThread main方法 : final String entryPoint = "android.app.ActivityThread";)
ProcessList -> startProcess
ZygoteProcess -> start
ZygoteProcess -> startViaZygote
zygoteSendArgsAndGetResult
attemptZygoteSendArgsAndGetResult


private Process.ProcessStartResult attemptZygoteSendArgsAndGetResult(
    ZygoteState zygoteState, String msgStr) throws ZygoteStartFailedEx {
    try {
        final BufferedWriter zygoteWriter = zygoteState.mZygoteOutputWriter;
        final DataInputStream zygoteInputStream = zygoteState.mZygoteInputStream;

        zygoteWriter.write(msgStr);
        zygoteWriter.flush();

        // Always read the entire result from the input stream to avoid leaving
        // bytes in the stream for future process starts to accidentally stumble
        // upon.
        Process.ProcessStartResult result = new Process.ProcessStartResult();
        result.pid = zygoteInputStream.readInt();
        result.usingWrapper = zygoteInputStream.readBoolean();

        if (result.pid < 0) {
            throw new ZygoteStartFailedEx("fork() failed");
        }

        return result;
    } catch (IOException ex) {
        zygoteState.close();
        Log.e(LOG_TAG, "IO Exception while communicating with Zygote - "
              + ex.toString());
        throw new ZygoteStartFailedEx(ex);
    }
}

```

Launcher通知AMS启动APP的MainActivity，也就是清单文件设置启动的Activity
AMS记录要启动的Activity信息，并且通知Launcher进入pause状态
Launcher进入pause状态后，通知AMS已经paused了，可以启动app了
app未开启过，所以会通过socket发送消息给AMS
AMS在SystemServer进程，该进程在启动时，执行ZygoteInit.main()后便进入runSelectLoop()循环体内，当有客户端连接时便会执行ZygoteConnection.runOnce()方法，再经过层层调用后fork出新的应用进程（handleChildProc）
并且在新进程中创建ActivityThread对象，执行其中的main函数方法


## ActivityThread

ActivityThread会做很多事，我们只分析和app启动与AMS相关的。

```
public static void main(String[] args) {
    // ...
    Looper.prepareMainLooper();

    ActivityThread thread = new ActivityThread();
    // 绑定Application
    thread.attach(false, startSeq);

    Looper.loop();
    // ...
}

private void attach(boolean system) { 
   sCurrentActivityThread = this;
   mSystemThread = system; // false
   if (!system) { // true
       ...
       // 获取 AMS，调用AMS的 attachApplication
       final IActivityManager mgr = ActivityManager.getService();
       try {
           mgr.attachApplication(mAppThread);
       } catch (RemoteException ex) {
           throw ex.rethrowFromSystemServer();
       }
       // Watch for getting close to heap limit.
       ...
   } else { // 系统进程处理逻辑
       ...
   }

   ...
}

```

## AMS 处理绑定Application

```
@Override
public final void attachApplication(IApplicationThread thread, long startSeq) {
    if (thread == null) {
        throw new SecurityException("Invalid application interface");
    }
    synchronized (this) {
        int callingPid = Binder.getCallingPid();
        final int callingUid = Binder.getCallingUid();
        final long origId = Binder.clearCallingIdentity();
        attachApplicationLocked(thread, callingPid, callingUid, startSeq);
        Binder.restoreCallingIdentity(origId);
    }
}

private final boolean attachApplicationLocked(IApplicationThread thread,
                                              int pid) {
    ProcessRecord app;
    // 根据pid 获取 对应 ProcessRecord
    // 新进程的名字
    final String processName = app.processName;

    ...
    thread.bindApplication(processName, appInfo, providerList, null, profilerInfo,
                           null, null, null, testMode,
                           mBinderTransactionTrackingEnabled, enableTrackAllocation,
                           isRestrictedBackupMode || !normalMode, app.isPersistent(),
                           new Configuration(app.getWindowProcessController().getConfiguration()),
                           app.compat, getCommonServicesLocked(app.isolated),
                           mCoreSettingsObserver.getCoreSettingsLocked(),
                           buildSerial, autofillOptions, contentCaptureOptions,
                           app.mDisabledCompatChanges);
    ...
    //查找所有可运行在该进程中的服务
    //检查这个进程中是否有下一个广播接收者
    //检查这个进程中是否有下一个备份代理
    //上述操作如果出现异常就杀死进程
    ...
    }


```

## ActivityThread.bindApplication

```
@Override
public final void bindApplication(String processName, ApplicationInfo appInfo,
                                  ProviderInfoList providerList, ComponentName instrumentationName,
                                  ProfilerInfo profilerInfo, Bundle instrumentationArgs,
                                  IInstrumentationWatcher instrumentationWatcher,
                                  IUiAutomationConnection instrumentationUiConnection, int debugMode,
                                  boolean enableBinderTracking, boolean trackAllocation,
                                  boolean isRestrictedBackupMode, boolean persistent, Configuration config,
                                  CompatibilityInfo compatInfo, Map services, Bundle coreSettings,
                                  String buildSerial, AutofillOptions autofillOptions,
                                  ContentCaptureOptions contentCaptureOptions, long[] disabledCompatChanges) {
    ...

    AppBindData data = new AppBindData();
    data.processName = processName;
    data.appInfo = appInfo;
    ...
        sendMessage(H.BIND_APPLICATION, data);
}

private void handleBindApplication(AppBindData data) {
    ...
    // application oncreate
    mInstrumentation.callApplicationOnCreate(app);
}

```

## 启动MainActivity


App启动时我们通过fork Zygote进程，创建了app进程，并做了一些application的绑定等等操作。
这些处理好后，就可以继续启动MainActivity。


```
ActivityStack -> resumeTopActivityInnerLocked
ActivityStackSupervisor -> startSpecificActivity
ActivityStackSupervisor -> realStartActivityLocked

private boolean resumeTopActivityInnerLocked(ActivityRecord prev, ActivityOptions options) {

    // ...
    
    // Since the start-process is asynchronous, if we already know the process of next
    // activity isn't running, we can start the process earlier to save the time to wait
    // for the current activity to be paused.
    final boolean isTop = this == taskDisplayArea.getFocusedStack();
    mAtmService.startProcessAsync(next, false /* knownToBeDead */, isTop,
                                  isTop ? "pre-top-activity" : "pre-activity");


    // ...

    mStackSupervisor.startSpecificActivity(next, true, true);

}

boolean realStartActivityLocked(ActivityRecord r, WindowProcessController proc,
                                boolean andResume, boolean checkConfig) throws RemoteException {

    mService.getLifecycleManager().scheduleTransaction(clientTransaction);
}

// 通过aidl进入app所在进程
// 启动MainActivity

ActivityThread -> scheduleTransaction
...
ActivityThread -> handleLaunchActivity
ActivityThread -> performLaunchActivity

```



## 4 重要的类
### ActvityRecord
用来存储activity的信息！

一个ActivityRecord对应一个Activity，一个Activity可能会有多个
### ActivityRecord
因为Activity可以被多次启动，这个主要取决于其启动模式。
### ActivityStack
则是用来管理ActivityRecord的，包含了多个ActivityRecord。

### ActivityStack
用来存储activity，也就是我们常说的activity栈。
ActivityStackSupervisor
用来管理ActivityStack！
Instrumentation
负责调用Activity和Application生命周期。
## 5 总结
AMS负责四大组件的启动，调度等工作，因为在不同进程，所以通信会基于binder或者socket。1、AMS是什么时候被初始化的？在手机开机，SystemServer进程启动后，就会启动初始化AMS。2、AMS与Zygote进程是通过什么通信的？

