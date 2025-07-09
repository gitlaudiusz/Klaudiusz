# ConvAI Services Integration Guide

**Date**: 2025-07-08  
**Dragon Main Services**: Ready for ConvAI Integration  
**Status**: All WebSocket services operational  

## 🚀 Available Services

### 1. Edge TTS WebSocket (Port 8003)
```javascript
const tts = new WebSocket('ws://localhost:8003/v1/synthesize');

// Send synthesis request
tts.send(JSON.stringify({
    text: "Dziękuję za wiadomość!",
    voice: "pl-PL-ZofiaNeural",
    rate: "+0%",
    pitch: "+0Hz",
    volume: "+0%"
}));

// Receive base64 audio
tts.onmessage = (event) => {
    const response = JSON.parse(event.data);
    if (response.type === 'audio') {
        const audioData = response.audio_base64;
        // Convert base64 to blob and play
        const audioBlob = new Blob([atob(audioData)], {type: 'audio/mpeg'});
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
    }
};
```

### 2. MLX Whisper WebSocket (Port 8002)
```javascript
const stt = new WebSocket('ws://localhost:8002/v1/transcribe');

// Send audio for transcription
stt.send(JSON.stringify({
    audio_base64: audioBase64Data,
    language: "pl",
    filename: "audio.wav"
}));

// Receive transcription
stt.onmessage = (event) => {
    const response = JSON.parse(event.data);
    if (response.type === 'transcription') {
        const text = response.text;
        const segments = response.segments;
        const processingTime = response.processing_time;
        console.log(`Transcribed: "${text}" (${processingTime}s)`);
    }
};
```

### 3. LLM Proxy WebSocket (Port 8001)
```javascript
const llm = new WebSocket('ws://localhost:8001/v1/chat/completions');

// Send chat completion request
llm.send(JSON.stringify({
    messages: [
        {role: "system", content: "Jesteś pomocnym asystentem mówiącym po polsku."},
        {role: "user", content: "Jak się masz?"}
    ],
    model: "LibraxisAI/Qwen3-14b-MLX-Q5",
    max_tokens: 4096
}));

// Receive completion
llm.onmessage = (event) => {
    const response = JSON.parse(event.data);
    if (response.type === 'completion') {
        const content = response.content;
        console.log(`LLM Response: "${content}"`);
    }
};
```

## 🔄 Complete Voice Conversation Loop

```javascript
class VoiceConversation {
    constructor() {
        this.tts = new WebSocket('ws://localhost:8003/v1/synthesize');
        this.stt = new WebSocket('ws://localhost:8002/v1/transcribe');
        this.llm = new WebSocket('ws://localhost:8001/v1/chat/completions');
        this.setupHandlers();
    }

    setupHandlers() {
        // STT: Audio → Text
        this.stt.onmessage = (event) => {
            const response = JSON.parse(event.data);
            if (response.type === 'transcription') {
                this.processUserText(response.text);
            }
        };

        // LLM: Text → Response
        this.llm.onmessage = (event) => {
            const response = JSON.parse(event.data);
            if (response.type === 'completion') {
                this.synthesizeResponse(response.content);
            }
        };

        // TTS: Text → Audio
        this.tts.onmessage = (event) => {
            const response = JSON.parse(event.data);
            if (response.type === 'audio') {
                this.playAudio(response.audio_base64);
            }
        };
    }

    // 1. User speaks → Audio captured
    processAudio(audioBase64) {
        this.stt.send(JSON.stringify({
            audio_base64: audioBase64,
            language: "pl"
        }));
    }

    // 2. STT → Text → LLM
    processUserText(text) {
        const messages = [
            {role: "system", content: "Jesteś przyjaźnie nastawionym asystentem."},
            {role: "user", content: text}
        ];
        
        this.llm.send(JSON.stringify({
            messages: messages,
            max_tokens: 4096
        }));
    }

    // 3. LLM Response → TTS
    synthesizeResponse(text) {
        this.tts.send(JSON.stringify({
            text: text,
            voice: "pl-PL-ZofiaNeural"
        }));
    }

    // 4. TTS → Audio → Play
    playAudio(audioBase64) {
        const audioBlob = new Blob([atob(audioBase64)], {type: 'audio/mpeg'});
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
    }
}

// Initialize voice conversation
const voiceChat = new VoiceConversation();
```

## 🔧 Audio Handling Solutions

### Problem: Cloudflare Binary WebSocket Issues
**Solution**: All services use base64 encoding to avoid binary frame problems.

### Audio Input Processing
```javascript
// Convert audio blob to base64
function audioToBase64(audioBlob) {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            const base64 = reader.result.split(',')[1]; // Remove data:audio/... prefix
            resolve(base64);
        };
        reader.readAsDataURL(audioBlob);
    });
}

// Usage in ConvAI
navigator.mediaDevices.getUserMedia({audio: true}).then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    const chunks = [];
    
    mediaRecorder.ondataavailable = (event) => {
        chunks.push(event.data);
    };
    
    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunks, {type: 'audio/wav'});
        const audioBase64 = await audioToBase64(audioBlob);
        voiceChat.processAudio(audioBase64);
    };
});
```

## 🎯 Integration Priorities

1. **Start with TTS**: Easiest to test - send text, get audio
2. **Add STT**: Test audio input → text output  
3. **Add LLM**: Test text → response generation
4. **Connect pipeline**: Audio → STT → LLM → TTS → Audio

## 🐛 Common Issues & Solutions

### TTS Issues
- **Empty audio**: Check text is not empty
- **Wrong voice**: Use `pl-PL-ZofiaNeural` for Polish
- **Playback fails**: Ensure base64 decode and blob creation

### STT Issues  
- **No transcription**: Check audio format and base64 encoding
- **Wrong language**: Always set `language: "pl"`
- **Poor quality**: Use WAV format, 16kHz sample rate

### LLM Issues
- **No response**: Check message format (OpenAI style)
- **Timeout**: Reduce max_tokens if responses are too long
- **Wrong language**: Add Polish system message

## 📊 Performance Expectations

- **STT Processing**: ~0.5-2s for 5-second audio
- **LLM Generation**: ~30-60s for thoughtful responses  
- **TTS Synthesis**: ~1-3s for short text
- **Total Loop Time**: ~35-65s per conversation turn

## 🔥 Next Steps for ConvAI Integration

1. **Test individual services** with simple WebSocket connections
2. **Implement audio recording** in ConvAI frontend
3. **Connect STT service** for voice input
4. **Add LLM integration** for response generation  
5. **Connect TTS service** for voice output
6. **Test full conversation loop** locally (bypass Cloudflare)
7. **Deploy to convai.libraxis.cloud** once working locally

All services are READY and WAITING for ConvAI integration! 🚀