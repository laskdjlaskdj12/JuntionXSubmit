import ast
import base64

from flask_socketio import send

from TTS.text_to_speech import tts
from controller import socketio
from data.tts.rep_tts_broad_cast_dto import ReplyTTSBroadCastDTO
from data.tts.req_tts_broad_cast_dto import RequestTTSBroadCastDTO


@socketio.on('tts')
def tts_controller(data):
    tts_broadcast_dto = RequestTTSBroadCastDTO("", "", "")
    if type(data) == str:
        dict_request_data_json = ast.literal_eval(data)
        tts_broadcast_dto = RequestTTSBroadCastDTO.from_dict(dict_request_data_json)
    else:
        tts_broadcast_dto = RequestTTSBroadCastDTO.from_dict(data)

    audio_data = tts(tts_broadcast_dto.text_data)
    base64_audio_data = base64.b64encode(audio_data).decode("UTF-8")
    reply_dto = ReplyTTSBroadCastDTO(tts_broadcast_dto.name, base64_audio_data)

    room = tts_broadcast_dto.room
    send(reply_dto.to_json(), room=tts_broadcast_dto.room)

    pass