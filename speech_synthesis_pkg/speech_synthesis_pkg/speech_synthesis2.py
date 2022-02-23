import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from gtts import gTTS
from io import BytesIO
from mpg123 import Mpg123, Out123


class SpeechSynthesis(Node):
    def __init__(self):
        super().__init__('speech_synthesis')

        self.logger = self.get_logger()
        self.logger.info('Start selection answer')
        self.mp3 = Mpg123()
        self.out = Out123()

        self.answer_sub = self.create_subscription(
            String, 'answer_text', self.answer_subscribe, 10)

    def answer_subscribe(self, msg):
        self.logger.info(f'Subscribe text "{msg.data}"')
        tts = gTTS(msg.data)
        start_time = time.perf_counter()
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        self.mp3.feed(fp.read())
        for frame in self.mp3.iter_frames(self.out.start):
            self.out.play(frame)
        end_time = time.perf_counter()
        self.logger.info(f'{end_time - start_time}')
        self.logger.info('Speeched text')


def main():
    rclpy.init()

    speech_synthesis = SpeechSynthesis()

    try:
        rclpy.spin(speech_synthesis)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
