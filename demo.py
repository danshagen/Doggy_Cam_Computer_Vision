'''Motion Detection with openCV.'''
import plac

@plac.opt('source', 'To use a webcam as a source, use 0 as source (default). \
    To use a video file, use its path as the source argument.')
@plac.flg('simple_diff', 'Enable the simple difference detection.', 'diff')
@plac.flg('background_subtraction', 'Enable the background subtraction algorithm.',
         'back')
def motion_detection(source='0', simple_diff=False, background_subtraction=False):
    '''
    Show motion detection algorithms: subtracting the previous frame 
    (simple_diff) and background subtraction. The source video is also shown.
    All videos are shown in seperate windows.

    The processing is paused when started and can be paused and unpaused with
    the space bar.

    Pressing 'q' while focusing one of the windows (and being unpaused) stops 
    the motion detection and quits the program.
    '''
    import cv2
    import numpy as np

    back_sub = cv2.createBackgroundSubtractorMOG2()

    # get video source
    if source == '0':
        source = 0
        out = 'out.avi'
    else:
        out = source.split('.')[0]
    video = cv2.VideoCapture(source)

    # Get current width of frame
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
    # Get current height of frame
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
    fps = video.get(cv2.CAP_PROP_FPS) * 4

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out_diff = cv2.VideoWriter('{}_diff.avi'.format(out), fourcc, 20.0, 
        (int(width*3),int(height)))

    # get one frame and populate before variable
    _,f = video.read()
    before = f.astype('int8')

    # flag for pausing and running
    paused = True

    # processing loop: runs until video is over or 'q' is pressed with a window
    # focused
    while(1):
        # get next frame
        _, frame = video.read()
        # when video is over, frame is None, exit gracefully
        if frame is None:
            break
        # convert to signed integer for subtraction (artefacts with unsigned
        # overflow/underflow happen otherwise)
        frame_int8 = frame.astype('int8')

        # show original source
        cv2.imshow('Source', frame)


        # use openCV background subtraction implementation
        if background_subtraction:
            back_sub_frame = back_sub.apply(frame, learningRate=-1)
            cv2.imshow('Background Subtraction', back_sub_frame)

        # calculate difference between frame before and now
        if simple_diff:
            diff_frame = np.abs(np.subtract(frame_int8, before))
            cv2.imshow('Difference', diff_frame)
            before = frame_int8
            out_diff.write(np.concatenate(
                (frame, diff_frame.astype('uint8'), cv2.cvtColor(back_sub_frame,cv2.COLOR_GRAY2RGB)), axis=1))

        # wait for exit keypress and continue the sampling
        if paused:
            while cv2.waitKey(1) & 0xFF != ord(' '):
                pass
            paused = False
        key = cv2.waitKey(100)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord(' '):
            paused = True

    video.release()
    out_diff.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    plac.call(motion_detection)