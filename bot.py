from src.openai_service.open_ai import get_ai_response
from src import stt_google_free
from src.websocket.controller import act_rigging
import asyncio
from src.azure_service.text_to_speech import TextToSpeech

class Vtuber:
    def __init__(self):
        pass

    def run(self):
        self.conversation()

    async def conversation(self):
        messages = []
        text_to_speech = TextToSpeech()

        while True:
            try:
                user_input = stt_google_free.stt_google()
                print(user_input)
                if user_input.lower() == "종료":
                    print("버튜버 AI: 대화를 종료합니다.")
                    break

                messages.append({"role": "user", "content": user_input})
                response = get_ai_response(messages)
                messages.append({"role": "assistant", "content": response})

                print("MAO :", response)
                
                tts = asyncio.create_task(text_to_speech.speak(response, pitch='+15%', rate="+25%"))
                await act_rigging(response)
                await tts
            except Exception as e:
                print(e)