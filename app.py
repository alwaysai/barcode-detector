import edgeiq
import time

def main():
    fps = edgeiq.FPS()
    barcode_scanner = edgeiq.BarcodeDetection()
    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                frame = video_stream.read()

                # Generate text to display on streamer
                streamer_text = ["Barcode Scanner"]

                # Localize and Decode the Barcode(s) if present in frame
                results = barcode_scanner.localize_decode(frame)

                # Draw the box around localized Barcode(s)
                image = results.markup_image()

                # Display decoded information from Barcode(s) on streamer
                for prediction in results.predictions:
                    streamer_text.append("{}: {}".format(
                            prediction.barcode_type, prediction.info))
                streamer.send_data(image, streamer_text)

                fps.update()

                if streamer.check_exit():
                    break

    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))
        print("Program Ending")


if __name__ == "__main__":
    main()
