class viewWindow(QtGui.QWidget):
    def __init__(self,name):
        QtGui.QWidget.__init__(self)
        self.name = name  # give the video to show up here

        self.mediaObject = Phonon.MediaObject(self)
        self.mediaObject.stateChanged.connect(self.stateChanged)
        self.videoWidget = Phonon.VideoWidget(self)
        Phonon.createPath(self.mediaObject, self.videoWidget)
        self.videoWidget.setMinimumSize(80, 80)

        self.metaInformationResolver = Phonon.MediaObject(self)
        self.mediaObject.setTickInterval(1000)  # send one signal/1000msec(1 sec),then show on the LCD time
        self.videoWidget.setScaleMode(0)  # control the size of the video(0 is default as the orginal size)

        self.connect(self.mediaObject, QtCore.SIGNAL('tick(qint64)'), self.tick)  #connect the time of media to tick fuction
        self.connect(self.mediaObject, QtCore.SIGNAL('stateChanged(Phonon::State, Phonon::State)'), self.stateChanged) # stateChange like play, stop,pause...
        self.connect(self.metaInformationResolver, QtCore.SIGNAL('stateChanged(Phonon::State, Phonon::State)'), self.metaStateChanged)
        self.connect(self.mediaObject, QtCore.SIGNAL('currentSourceChanged(Phonon::MediaSource)'), self.sourceChanged)

        self.setupActions()  # initial all the actions,
        self.video_id = self.videoWidget.winId()  # get the frame of video


        bar = QtGui.QToolBar()
        bar.addAction(self.playAction)
        bar.addAction(self.pauseAction)
        bar.addAction(self.stopAction)
        #bar.addAction(self.loadAction)
        bar.addAction(self.screenshotAction)
        bar.addAction(self.saveAction)
        #bar.addAction(self.fullAction)
        bar.addAction(self.deleteAction)

        self.seekSlider = Phonon.SeekSlider(self)         # build a seekSlider
        self.seekSlider.setMediaObject(self.mediaObject)  # seekSlider connect to the video

        # define the palette to change color
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Light, QtCore.Qt.darkGray)

        #create LCD
        self.timeLcd = QtGui.QLCDNumber()
        self.timeLcd.setPalette(palette)


        # build seek layer in widget
        seekerLayout = QtGui.QHBoxLayout()
        seekerLayout.addWidget(self.seekSlider)
        seekerLayout.addWidget(self.timeLcd)
        self.timeLcd.display("00:00")  # initial LCD play

        playbackLayout = QtGui.QHBoxLayout()
        playbackLayout.addWidget(bar)
        playbackLayout.addStretch()

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.videoWidget, 1)

        layout.addLayout(seekerLayout)
        layout.addLayout(playbackLayout)

        self.addFiles()

        self.shortcutFull = QtGui.QShortcut(self)
        self.shortcutFull.setKey(QtGui.QKeySequence('Esc'))
        self.shortcutFull.setContext(QtCore.Qt.ApplicationShortcut)
        self.shortcutFull.activated.connect(self.handleFullScreen)

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.videoWidget.isFullScreen():
                self.videoWidget.exitFullScreen()
            else:
                self.videoWidget.enterFullScreen()

    def handleFullScreen(self):
         #videoWidget = self.ui.videoPlayer.videoWidget()
         #self.videoWidget.exitFullScreen()

         if self.videoWidget.isFullScreen():
             self.videoWidget.exitFullScreen()
         else:
             self.videoWidget.enterFullScreen()


    def full(self):
           # videoWidget = self.ui.videoPlayer.videoWidget()
            if not self.videoWidget.isFullScreen():
                self.videoWidget.enterFullScreen()
            else:
                self.videoWidget.exitFullScreen()

    def screenshot(self):
            #self.video_id = self.videoWidget.winId()
            self.screenshot = Screenshot(self.video_id)
            self.screenshot.show()

    def addFiles(self):
            files = self.name
            if not files:
                return
            self.source = Phonon.MediaSource(files)

            if self.source:
                self.metaInformationResolver.setCurrentSource(self.source)

    def sizeHint(self):
            return QtCore.QSize(600, 450)

    def stateChanged(self, newState, oldState):
            if newState == Phonon.ErrorState:
                if self.mediaObject.errorType() == Phonon.FatalError:
                    QtGui.QMessageBox.warning(self, self.tr("Fatal Error"),self.mediaObject.errorString())
                else:
                    QtGui.QMessageBox.warning(self, self.tr("Error"),self.mediaObject.errorString())

            elif newState == Phonon.PlayingState:
                self.playAction.setEnabled(False)
                self.pauseAction.setEnabled(True)
                self.stopAction.setEnabled(True)

            elif newState == Phonon.StoppedState:
                self.stopAction.setEnabled(False)
                self.playAction.setEnabled(True)
                self.pauseAction.setEnabled(False)
                self.timeLcd.display("00:00")

            elif newState == Phonon.PausedState:
                self.pauseAction.setEnabled(False)
                self.stopAction.setEnabled(True)
                self.playAction.setEnabled(True)

    def tick(self, time):
            displayTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
            self.timeLcd.display(displayTime.toString('mm:ss'))

    def sourceChanged(self, source):
            self.timeLcd.display("00:00")

    def metaStateChanged(self, newState, oldState):
            if newState == Phonon.ErrorState:
                QtGui.QMessageBox.warning(self, self.tr("Error opening files"),
                        self.metaInformationResolver.errorString())

            self.mediaObject.setCurrentSource(self.metaInformationResolver.currentSource())

            source = self.metaInformationResolver.currentSource()

    def handleButton(self):
        if self.mediaObject.state() == Phonon.PlayingState:
            self.mediaObject.stop()
        else:
            path = QtGui.QFileDialog.getOpenFileName(self)
            if path:
                self.mediaObject.setCurrentSource(Phonon.MediaSource(path))
                self.mediaObject.play()

    def saveFiles(self):
            format = QtCore.QString("avi")

            initialPath = QtCore.QDir.currentPath() + self.tr("/untitled.") + format

            fileName = QtGui.QFileDialog.getSaveFileName(self, self.tr("Save As"),
                                   initialPath,
                                   self.tr("%1 Files (*.%2);; .mp4 ;; .wmv;; .mkv;; .flv;; All Files (*)") # save as multiple format
                                       .arg(format.toUpper())
                                       .arg(format))
            #ffmpeg.convert(self.name,fileName)
            if not fileName.isEmpty():
                self.originalPixmap.save(fileName, str(format))



    def handleStateChanged(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.button.setText('Stop')
        elif (newstate != Phonon.LoadingState and
              newstate != Phonon.BufferingState):
            self.button.setText('Choose File')
            if newstate == Phonon.ErrorState:
                source = self.mediaObject.currentSource().fileName()
                print ('ERROR: could not play:', source.toLocal8Bit().data())
                print ('  %s' % self.mediaObject.errorString().toLocal8Bit().data())


    def setupActions(self):

            self.playAction = QtGui.QAction(QtGui.QIcon("play.jpg"), self.tr("Play"), self)
            #self.playAction.setShortcut(self.tr("Crl+P"))
            self.playAction.setDisabled(True)

            self.pauseAction = QtGui.QAction(QtGui.QIcon("pause.jpg"), self.tr("Pause"), self)
            self.pauseAction.setShortcut(self.tr("space"))
            self.pauseAction.setDisabled(True)

            self.stopAction = QtGui.QAction(QtGui.QIcon("stop.jpg"), self.tr("Stop"), self)
            #self.stopAction.setShortcut(self.tr("Ctrl+S"))
            self.stopAction.setDisabled(True)

            self.loadAction = QtGui.QAction(QtGui.QIcon("load.jpg"), self.tr("Load"), self)
            #self.loadAction.setShortcut(self.tr("Ctrl+L"))
            self.loadAction.setDisabled(False)

            self.deleteAction = QtGui.QAction(QtGui.QIcon("delete.jpg"), self.tr("Delete"), self)
            #self.loadAction.setShortcut(self.tr("Ctrl+L"))
            self.loadAction.setDisabled(False)

            self.screenshotAction = QtGui.QAction(QtGui.QIcon("screenshot.jpg"), self.tr("screenshot"), self)
            #self.loadAction.setShortcut(self.tr("Ctrl+L"))
            self.screenshotAction.setDisabled(False)

            self.saveAction = QtGui.QAction(QtGui.QIcon("save.png"), self.tr("save"), self)
            #self.loadAction.setShortcut(self.tr("Ctrl+L"))
            self.saveAction.setDisabled(False)

            self.fullAction = QtGui.QAction(QtGui.QIcon("fullscreen.jpg"),self.tr("Full screen"), self)
            self.saveAction.setDisabled(False)
            self.fullAction.setShortcut(self.tr("Ctrl+F11"))

            self.connect(self.playAction, QtCore.SIGNAL('triggered()'),self.mediaObject, QtCore.SLOT('play()'))
            self.connect(self.pauseAction, QtCore.SIGNAL('triggered()'),self.mediaObject, QtCore.SLOT('pause()'))
            self.connect(self.stopAction, QtCore.SIGNAL('triggered()'),self.mediaObject, QtCore.SLOT('stop()'))
            self.connect(self.loadAction, QtCore.SIGNAL('triggered()'), self.handleButton)
            self.connect(self.deleteAction, QtCore.SIGNAL('triggered()'), self.deleteLater)
            self.connect(self.screenshotAction, QtCore.SIGNAL('triggered()'), self.screenshot)
            self.connect(self.saveAction, QtCore.SIGNAL('triggered()'), self.saveFiles)
            self.connect(self.fullAction, QtCore.SIGNAL('triggered()'), self.full)
