"""
Composition Assistant Workflow Diagram Generator

Generates visual representations of the audio processing and music transformation workflow.
"""

def generate_ascii_diagram():
    """Generate ASCII art diagram of the Composition Assistant workflow."""
    return """
╔══════════════════════════════════════════════════════════════════════════════════════════╗
║                      COMPOSITION ASSISTANT - WORKFLOW DIAGRAM                            ║
╚══════════════════════════════════════════════════════════════════════════════════════════╝

┌──────────┐
│   USER   │ ◄─────────────────────────────────────────────────────────────┐
└────┬─────┘                                                               │
     │ Audio File (WAV)                                                    │
     │ + User Prompt                                                       │ Modified WAV
     ▼                                                                     │
═══════════════════════════════════════════════════════════════════════════▼═══════════════
                              FASTAPI SERVER (API Gateway)
════════════════════════════════════════════════════════════════════════════════════════════
     │
     ▼ Stage 1: FILE UPLOAD
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌──────────────────┐                                                                    │
│ │  FILE HANDLER    │  • Receive uploaded WAV file                                       │
│ │  /process-wav/   │  • Save to tmp/input/                                              │
│ └────────┬─────────┘  • Extract user prompt/goal                                        │
└──────────┼──────────────────────────────────────────────────────────────────────────────┘
           │ Audio Path + Prompt
           ▼ Stage 2: AUDIO TRANSCRIPTION
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌───────────────────────────────────────────────────────────────────────────────────┐   │
│ │  TRANSCRIPTION MODULE - basic-pitch                                               │   │
│ │                                                                                   │   │
│ │  ┌────────────────────────────────────────────────────────────────────────────┐   │   │
│ │  │ transcribe_audio(audio_file)                                               │   │   │
│ │  │                                                                            │   │   │
│ │  │   WAV File ──► basic-pitch ──► MIDI Object                                 │   │   │
│ │  │                    │                                                       │   │   │
│ │  │              ┌─────┴─────┐                                                 │   │   │
│ │  │              │  Neural   │                                                 │   │   │
│ │  │              │  Network  │                                                 │   │   │
│ │  │              │  Model    │                                                 │   │   │
│ │  │              └───────────┘                                                 │   │   │
│ │  │                                                                            │   │   │
│ │  │   Output: MIDI object with note events                                     │   │   │
│ │  └────────────────────────────────────────────────────────────────────────────┘   │   │
│ └───────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
           │ MIDI Object
           ▼ Stage 3: MIDI TO JSON CONVERSION
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌───────────────────────────────────────────────────────────────────────────────────┐   │
│ │  MIDI-JSON CONVERTER                                                              │   │
│ │                                                                                   │   │
│ │  ┌────────────────────────────────────────────────────────────────────────────┐   │   │
│ │  │ midi_to_json(midi_obj)                                                     │   │   │
│ │  │                                                                            │   │   │
│ │  │   MIDI Object ──► Note Event Extraction ──► JSON Array                     │   │   │
│ │  │                                                                            │   │   │
│ │  │   Output: [                                                                │   │   │
│ │  │     {"pitch": 60, "start": 0.0, "end": 0.5, "velocity": 100},              │   │   │
│ │  │     {"pitch": 64, "start": 0.5, "end": 1.0, "velocity": 110},              │   │   │
│ │  │     ...                                                                    │   │   │
│ │  │   ]                                                                        │   │   │
│ │  └────────────────────────────────────────────────────────────────────────────┘   │   │
│ └───────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
           │ JSON Note Events
           ▼ Stage 4: LLM PROCESSING
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌───────────────────────────────────────────────────────────────────────────────────┐   │
│ │  LLM AGENT - Ollama (qwen2.5:7b)                                                  │   │
│ │                                                                                   │   │
│ │  ┌─────────────────────────────────────────────────────────────────────────────┐  │   │
│ │  │ SYSTEM PROMPT                                                               │  │   │
│ │  │ ┌─────────────────────────────────────────────────────────────────────────┐ │  │   │
│ │  │ │ You are a music-theory assistant.                                       │ │  │   │
│ │  │ │ • Interval changes (transpose notes)                                    │ │  │   │
│ │  │ │ • Modal shifts (change scale)                                           │ │  │   │
│ │  │ │ • Rhythmic alterations (adjust timing)                                  │ │  │   │
│ │  │ │ • Register changes (octave shifts)                                      │ │  │   │
│ │  │ └─────────────────────────────────────────────────────────────────────────┘ │  │   │
│ │  └─────────────────────────────────────────────────────────────────────────────┘  │   │
│ │                                                                                   │   │
│ │  ┌─────────────────────────────────────────────────────────────────────────────┐  │   │
│ │  │ USER PROMPT                                                                 │  │   │
│ │  │ ┌─────────────────────────────────────────────────────────────────────────┐ │  │   │
│ │  │ │ Goal: {user_prompt}                                                     │ │  │   │
│ │  │ │ MIDI summary: {json_notes}                                              │ │  │   │
│ │  │ │ Return transformation actions.                                          │ │  │   │
│ │  │ └─────────────────────────────────────────────────────────────────────────┘ │  │   │
│ │  └─────────────────────────────────────────────────────────────────────────────┘  │   │
│ │                                                                                   │   │
│ │                              ▼                                                    │   │
│ │  ┌─────────────────────────────────────────────────────────────────────────────┐  │   │
│ │  │ LLM OUTPUT: Modified JSON Note Events                                       │  │   │
│ │  │ [{"pitch": 62, "start": 0.0, "end": 0.5, "velocity": 100}, ...]             │  │   │
│ │  └─────────────────────────────────────────────────────────────────────────────┘  │   │
│ └───────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
           │ Modified JSON Note Events
           ▼ Stage 5: OUTPUT GENERATION
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌───────────────────────────────────────────────────────────────────────────────────┐   │
│ │  JSON TO WAV CONVERTER                                                            │   │
│ │                                                                                   │   │
│ │  ┌────────────────────────────────────────────────────────────────────────────┐   │   │
│ │  │ json_to_wav(edited_notes, output_path)                                     │   │   │
│ │  │                                                                            │   │   │
│ │  │   JSON Notes ──► MIDI Object ──► FluidSynth ──► WAV File                   │   │   │
│ │  │                       │              │                                     │   │   │
│ │  │                       │         ┌────┴────┐                                │   │   │
│ │  │                       │         │FluidR3  │                                │   │   │
│ │  │                       │         │Soundfont│                                │   │   │
│ │  │                       │         └─────────┘                                │   │   │
│ │  │                       │                                                    │   │   │
│ │  │   Output: tmp/output/agent_output.wav                                      │   │   │
│ │  └────────────────────────────────────────────────────────────────────────────┘   │   │
│ └───────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
           │ WAV File Path
           ▼ Stage 6: FILE DOWNLOAD
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌──────────────────┐                                                                    │
│ │  DOWNLOAD API    │  • Serve generated WAV file                                        │
│ │  /download/      │  • Return to user                                                  │
│ └──────────────────┘                                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════════════

SUPPORTED TRANSFORMATIONS:
• Interval Changes     - Transpose notes up or down by semitones
• Modal Shifts         - Change notes to fit a different musical scale/mode
• Rhythmic Alterations - Adjust note start/end times (tempo, timing)
• Register Changes     - Move notes up or down by octaves

DATA FLOW:
WAV ──► MIDI ──► JSON ──► LLM ──► JSON ──► MIDI ──► WAV

LEGEND:
───── Sequential Flow          ═════ Component Boundary
┌────┐ Processing Unit         ──►── Data Flow Direction
"""


def generate_mermaid_diagram():
    """Generate Mermaid diagram of the workflow."""
    return """
graph TB
    User([User]) -->|WAV + Prompt| API[FastAPI Server<br/>/process-wav/]
    
    subgraph UploadPhase["Stage 1: File Upload"]
        API --> FileHandler[File Handler]
        FileHandler -->|Save| TmpInput[(tmp/input/)]
    end
    
    subgraph TranscriptionPhase["Stage 2: Audio Transcription"]
        TmpInput --> Transcribe[Transcription Module<br/>basic-pitch]
        Transcribe -->|Neural Network| MIDI[MIDI Object]
    end
    
    subgraph ConversionPhase["Stage 3: MIDI to JSON"]
        MIDI --> MidiJson[midi_to_json]
        MidiJson --> NotesJson[JSON Note Events<br/>pitch, start, end, velocity]
    end
    
    subgraph LLMPhase["Stage 4: LLM Processing"]
        NotesJson --> LLM[LLM Agent<br/>Ollama qwen2.5:7b]
        
        subgraph SystemPrompt["System Prompt"]
            SP1[Music Theory Assistant]
            SP2[Interval Changes]
            SP3[Modal Shifts]
            SP4[Rhythmic Alterations]
            SP5[Register Changes]
        end
        
        LLM --> Modified[Modified JSON Notes]
    end
    
    subgraph OutputPhase["Stage 5: Output Generation"]
        Modified --> JsonWav[json_to_wav]
        JsonWav --> FluidSynth[FluidSynth<br/>+ FluidR3 Soundfont]
        FluidSynth --> OutputWav[(tmp/output/<br/>agent_output.wav)]
    end
    
    subgraph DownloadPhase["Stage 6: Download"]
        OutputWav --> DownloadAPI[Download API<br/>/download/]
    end
    
    DownloadAPI -->|Modified WAV| User
    
    style User fill:#e1f5e1
    style API fill:#ffe1e1
    style Transcribe fill:#e1e1ff
    style LLM fill:#ffe1ff
    style FluidSynth fill:#ffffe1
    style OutputWav fill:#e1ffff
"""


def generate_html_diagram():
    """Generate an HTML file with both diagrams."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Composition Assistant - Workflow Diagram</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1, h2, h3 {{
            color: #333;
        }}
        .diagram-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .ascii-diagram {{
            background: #1e1e1e;
            color: #00ff00;
            padding: 20px;
            border-radius: 4px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 11px;
            line-height: 1.3;
        }}
        .execution-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .detail-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }}
        .stage-indicator {{
            background: #28a745;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}
        code {{
            background: #f1f1f1;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f8f9fa;
        }}
    </style>
</head>
<body>
    <h1>🎵 Composition Assistant - Workflow Diagram</h1>
    
    <div class="diagram-container">
        <h2>Interactive Mermaid Diagram</h2>
        <div class="mermaid">
{generate_mermaid_diagram()}
        </div>
    </div>
    
    <div class="diagram-container">
        <h2>ASCII Flow Diagram</h2>
        <pre class="ascii-diagram">{generate_ascii_diagram()}</pre>
    </div>
    
    <div class="diagram-container">
        <h2>Processing Stages</h2>
        <div class="execution-details">
            <div class="detail-card">
                <h3>📤 Stage 1: File Upload</h3>
                <span class="stage-indicator">INPUT</span>
                <ul>
                    <li><b>Endpoint:</b> POST /process-wav/</li>
                    <li><b>Input:</b> WAV audio file + text prompt</li>
                    <li><b>Storage:</b> tmp/input/</li>
                </ul>
            </div>
            
            <div class="detail-card">
                <h3>🎼 Stage 2: Audio Transcription</h3>
                <span class="stage-indicator">TRANSCRIBE</span>
                <ul>
                    <li><b>Library:</b> basic-pitch</li>
                    <li><b>Process:</b> Neural network audio analysis</li>
                    <li><b>Output:</b> MIDI object with note events</li>
                </ul>
            </div>
            
            <div class="detail-card">
                <h3>🔄 Stage 3: MIDI to JSON</h3>
                <span class="stage-indicator">CONVERT</span>
                <ul>
                    <li><b>Function:</b> midi_to_json()</li>
                    <li><b>Output Format:</b> JSON array of note objects</li>
                    <li><b>Fields:</b> pitch, start, end, velocity</li>
                </ul>
            </div>
            
            <div class="detail-card">
                <h3>🤖 Stage 4: LLM Processing</h3>
                <span class="stage-indicator">AI</span>
                <ul>
                    <li><b>Model:</b> Ollama qwen2.5:7b</li>
                    <li><b>Role:</b> Music theory assistant</li>
                    <li><b>Capabilities:</b>
                        <ul>
                            <li>Interval changes</li>
                            <li>Modal shifts</li>
                            <li>Rhythmic alterations</li>
                            <li>Register changes</li>
                        </ul>
                    </li>
                </ul>
            </div>
            
            <div class="detail-card">
                <h3>🔊 Stage 5: Output Generation</h3>
                <span class="stage-indicator">SYNTHESIZE</span>
                <ul>
                    <li><b>Function:</b> json_to_wav()</li>
                    <li><b>Synthesizer:</b> FluidSynth</li>
                    <li><b>Soundfont:</b> FluidR3_GM</li>
                    <li><b>Output:</b> WAV audio file</li>
                </ul>
            </div>
            
            <div class="detail-card">
                <h3>📥 Stage 6: Download</h3>
                <span class="stage-indicator">OUTPUT</span>
                <ul>
                    <li><b>Endpoint:</b> GET /download/{{filename}}</li>
                    <li><b>Format:</b> audio/wav</li>
                    <li><b>Location:</b> tmp/output/</li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="diagram-container">
        <h2>Supported Music Transformations</h2>
        <table>
            <thead>
                <tr>
                    <th>Transformation</th>
                    <th>Description</th>
                    <th>Example</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Interval Changes</strong></td>
                    <td>Transpose notes up or down by semitones</td>
                    <td>"Transpose up by 3 semitones"</td>
                </tr>
                <tr>
                    <td><strong>Modal Shifts</strong></td>
                    <td>Change notes to fit a different musical scale or mode</td>
                    <td>"Change to Dorian mode"</td>
                </tr>
                <tr>
                    <td><strong>Rhythmic Alterations</strong></td>
                    <td>Adjust note start/end times to change tempo or timing</td>
                    <td>"Double the tempo"</td>
                </tr>
                <tr>
                    <td><strong>Register Changes</strong></td>
                    <td>Move notes up or down by octaves</td>
                    <td>"Move melody up one octave"</td>
                </tr>
            </tbody>
        </table>
    </div>
    
    <div class="diagram-container">
        <h2>API Endpoints</h2>
        <table>
            <thead>
                <tr>
                    <th>Endpoint</th>
                    <th>Method</th>
                    <th>Description</th>
                    <th>Parameters</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>/process-wav/</code></td>
                    <td>POST</td>
                    <td>Process an audio file with AI transformation</td>
                    <td>file (WAV), prompt (text)</td>
                </tr>
                <tr>
                    <td><code>/download/{{filename}}</code></td>
                    <td>GET</td>
                    <td>Download the processed audio file</td>
                    <td>filename (string)</td>
                </tr>
                <tr>
                    <td><code>/metrics</code></td>
                    <td>GET</td>
                    <td>Prometheus-compatible metrics</td>
                    <td>None</td>
                </tr>
                <tr>
                    <td><code>/workflow-diagram</code></td>
                    <td>GET</td>
                    <td>Interactive workflow diagram</td>
                    <td>None</td>
                </tr>
                <tr>
                    <td><code>/health</code></td>
                    <td>GET</td>
                    <td>Health check endpoint</td>
                    <td>None</td>
                </tr>
            </tbody>
        </table>
    </div>
    
    <div class="diagram-container">
        <h2>Data Flow Summary</h2>
        <p style="font-size: 18px; text-align: center; font-family: monospace;">
            WAV ──► MIDI ──► JSON ──► LLM ──► JSON ──► MIDI ──► WAV
        </p>
    </div>
</body>
</html>"""
    return html_content


if __name__ == "__main__":
    # Save ASCII diagram
    with open("workflow_diagram.txt", "w", encoding="utf-8") as f:
        f.write(generate_ascii_diagram())
    
    # Save Mermaid diagram
    with open("workflow_diagram.mmd", "w", encoding="utf-8") as f:
        f.write(generate_mermaid_diagram())
    
    # Save HTML with both diagrams
    with open("workflow_diagram.html", "w", encoding="utf-8") as f:
        f.write(generate_html_diagram())
    
    print("Workflow diagrams generated:")
    print("  - workflow_diagram.txt (ASCII)")
    print("  - workflow_diagram.mmd (Mermaid)")
    print("  - workflow_diagram.html (Interactive HTML)")
