package eeg;

import java.io.FileWriter;
import java.io.IOException;
import java.util.logging.Logger;

import com.github.fommil.emokit.EmotivListener;
import com.github.fommil.emokit.Packet;

/**
 * Write packets to file.
 *
 */
public class FileWritingEmotivListener implements EmotivListener {
  private final static Logger LOGGER =
      Logger.getLogger(FileWritingEmotivListener.class .getName());

  private final FileWriter mFile;
  
  public FileWritingEmotivListener(String file) throws IOException {
      mFile = new FileWriter(file);
  }

  @Override
  public void connectionBroken() {
    // Close file; log upon failure.
    try {
      mFile.close();
    } catch (Exception e) {
      LOGGER.warning(e.getMessage());
    }
  }

  @Override
  public void receivePacket(Packet arg0) {
    // TODO Do a proper CSV write.
    try {
      mFile.append(arg0.toString());
    } catch (IOException e) {
      LOGGER.warning(e.getMessage());
    }
  }

  /**
   * Should be called when file write is complete.
   */
  public void close() {
    // Close file; log upon failure.
    try {
      mFile.close();
    } catch (Exception e) {
      LOGGER.warning(e.getMessage());
    }
  }
}
