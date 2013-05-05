package eeg;

import java.io.IOException;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

import com.github.fommil.emokit.Emotiv;
import com.github.fommil.emokit.EmotivListener;
import com.github.fommil.emokit.Packet;

public class EegRecorder {
  public static void main(String[] args) throws IOException, InterruptedException {
    System.out.println("Opening connection to Emotiv EPOC headset...");

    // Setup necessary resources.
    final Emotiv emotiv = new Emotiv();
    final Condition condition = new ReentrantLock().newCondition();

    // Open a connection to the EEG headset.
    emotiv.addEmotivListener(new EmotivListener() {
      public void receivePacket(Packet packet) {
      }

      public void connectionBroken() {
        condition.signal();
      }
    });

    emotiv.start();
    condition.await();
    emotiv.close();
  }
}
