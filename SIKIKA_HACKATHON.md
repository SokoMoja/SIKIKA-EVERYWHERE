# SIKIKA — Hackathon Build Document

> **"SIKIKA"** — Swahili for *"to be heard"*
> Real-time AI-powered lecture accessibility for deaf and blind university students.

---

## Table of Contents

1. [The Problem](#1-the-problem)
2. [Why This Matters](#2-why-this-matters)
3. [The Innovation](#3-the-innovation)
4. [How It Works](#4-how-it-works)
5. [System Architecture](#5-system-architecture)
6. [Data Models](#6-data-models)
7. [Feature Specifications](#7-feature-specifications)
8. [Tech Stack](#8-tech-stack)
9. [48-Hour Build Plan](#9-48-hour-build-plan)
10. [Demo Script](#10-demo-script)
11. [Addressing the Problem Statements](#11-addressing-the-problem-statements)
12. [Uniqueness Defense](#12-uniqueness-defense)
13. [Pitch Talking Points](#13-pitch-talking-points)

---

## 1. The Problem

### The Physics of Exclusion

A lecture is **sound waves** from a lecturer's mouth and **visual information** on a board/screen.

- A **deaf student** cannot access the sound waves.
- A **blind student** cannot access the visual information.
- The current solution: **human sign language interpreters** and **human note-takers**.

### Why the Current Solution is Broken

| Problem | Reality |
|---|---|
| **Interpreter scarcity** | Kenya has ~200 certified sign language interpreters for 50M+ people. Universities compete for a tiny pool. |
| **Subject-matter accuracy** | Interpreters sign "the thing connects to the other thing" because they can't sign "polymorphism" or "mitochondrial membrane." Technical accuracy is destroyed. |
| **Cost** | A professional interpreter costs $25–60/hour. 20 deaf students across 5 courses = $100K–$300K/year. Most African universities can't afford this. |
| **Availability** | Interpreter doesn't show up → Deaf student sits in class for 90 minutes learning NOTHING. This happens regularly. |
| **Information loss** | Human interpreters drop ~20–30% of content, especially at speed. They can't pause the lecturer. |
| **No solution for blind students** | Braille materials take days/weeks to produce. Blind students are permanently studying BEHIND the class. |
| **Stigma** | Having an interpreter standing next to you singles you out. Many students avoid using support services. |
| **One-way only** | Interpreters convert lecturer → student. But the deaf student can't easily ask questions back. Two-way communication is broken. |

### The Scale

- **15%** of the global population lives with some form of disability (~1.3 billion people)
- **Sub-Saharan Africa**: ~80 million people with disabilities
- University disability enrollment is **rising** due to inclusion policies, but support infrastructure is **NOT keeping up**
- The math is impossible: **You cannot hire enough human interpreters. The supply does not exist.**

---

## 2. Why This Matters

This is not a convenience problem. This is a **human rights issue**.

- The UN Convention on the Rights of Persons with Disabilities (Article 24) guarantees the right to inclusive education
- Most African countries have signed this convention
- Universities are **legally obligated** to provide accommodations — but they physically cannot
- Every lecture without access is a lecture where a disabled student **paid tuition and received nothing**

### The Affected Population

| Group | Size | Current Reality |
|---|---|---|
| Deaf/hard-of-hearing university students | Hundreds of thousands across Africa | Dependent on scarce, expensive interpreters. Miss content daily. |
| Blind/low-vision university students | Hundreds of thousands across Africa | Materials arrive late. Visual content (slides, board) is inaccessible. |
| International students (language barrier) | Millions | Struggle with lectures in non-native language. No real-time translation. |
| ALL students | Everyone | Could benefit from searchable lecture transcripts and study materials. |

---

## 3. The Innovation

### What SIKIKA Is

> A real-time AI lecture translator that converts live lectures into accessible formats — smart captions, audio descriptions, sign language visuals — on the student's own device, with zero human interpreters needed.

### What SIKIKA Is NOT

- ❌ Not an LMS (doesn't deliver course content)
- ❌ Not a video conferencing tool (lectures happen in physical classrooms)
- ❌ Not a simple speech-to-text app (it adds academic intelligence on top)
- ❌ Not a replacement for education — it's the **bridge** that makes education accessible

### The Key Insight

The individual AI technologies exist (speech-to-text, text-to-speech, image description, translation). **No one has combined them into a single, university-focused, classroom-embedded accessibility solution for African higher education.**

We're not inventing new AI. We're creating the **integration that should exist but doesn't**.

---

## 4. How It Works

### The Flow (Simple Version)

```
LECTURER                          STUDENTS
speaks into                       open browser on
phone/laptop mic                  phone/laptop
      │                                │
      ▼                                ▼
[Browser captures                 [Enter session
 audio via Web                     code: XK47]
 Speech API]                           │
      │                                │
      ▼                                ▼
[Real-time                        [Choose mode:]
 transcription]                        │
      │                          ┌─────┼─────────┐
      ▼                          ▼     ▼         ▼
[Django Server ◄── WebSocket ──► 🔤    🔊       🤟
 broadcasts to                Caption  Audio    Sign
 all connected                 Mode    Mode     Mode
 students]
```

### Step-by-Step

1. **Lecturer** opens SIKIKA in their browser, creates a session, gets a 4-character join code
2. **Students** open SIKIKA on their own devices, enter the join code
3. Each student selects their preferred accessibility mode
4. Lecturer clicks **"Start Live Session"** → browser requests microphone access
5. **Web Speech API** (built into Chrome/Edge, FREE) transcribes speech in real-time
6. Transcribed text is sent via **WebSocket** to the Django server
7. Server processes the text (term detection, formatting) and **broadcasts** to all connected students
8. Each student's device renders the content according to their chosen mode:
   - **Caption Mode**: Live scrolling captions with highlighted technical terms and definitions
   - **Audio Mode**: AI-generated descriptions of slides read aloud through earphones
   - **Sign Mode**: Captions displayed alongside sign language GIF animations for key terms
9. When the lecture ends, the full transcript is saved and downloadable

### Zero Cost, Zero Hardware, Zero Installs

- Web Speech API = **free** (runs in browser)
- WebSocket via Django Channels = **free** (open source)
- Text-to-Speech = **free** (browser Speech Synthesis API)
- Works on **any phone or laptop** with a browser
- **No app install** — it's a web app
- The only "hardware" needed is the lecturer's existing phone or laptop microphone

---

## 5. System Architecture

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         SIKIKA SYSTEM                             │
│                                                                   │
│  ┌─────────────────┐     ┌──────────────────┐                    │
│  │  LECTURER CLIENT │     │  Django Server    │                    │
│  │  (Browser)       │     │                  │                    │
│  │                  │     │  ┌────────────┐  │   ┌──────────────┐│
│  │  Web Speech API  │────▶│  │  Channels  │  │──▶│ STUDENT      ││
│  │  (mic → text)    │ WS  │  │  (WebSocket│  │WS │ CLIENT 1     ││
│  │                  │     │  │   router)  │  │   │ Caption Mode ││
│  │  Slide Upload    │────▶│  └────────────┘  │   └──────────────┘│
│  │  (HTTP POST)     │HTTP │                  │                    │
│  └─────────────────┘     │  ┌────────────┐  │   ┌──────────────┐│
│                           │  │  Views     │  │──▶│ STUDENT      ││
│                           │  │  (Auth,    │  │WS │ CLIENT 2     ││
│                           │  │   Session, │  │   │ Audio Mode   ││
│                           │  │   Upload)  │  │   └──────────────┘│
│                           │  └────────────┘  │                    │
│                           │                  │   ┌──────────────┐│
│                           │  ┌────────────┐  │──▶│ STUDENT      ││
│                           │  │  Models    │  │WS │ CLIENT 3     ││
│                           │  │  (DB)      │  │   │ Sign Mode    ││
│                           │  └────────────┘  │   └──────────────┘│
│                           └──────────────────┘                    │
│                                    │                              │
│                           ┌────────▼─────────┐                    │
│                           │  SQLite Database  │                    │
│                           │  (Sessions,       │                    │
│                           │   Transcripts,    │                    │
│                           │   Users, Slides,  │                    │
│                           │   Glossary)       │                    │
│                           └──────────────────┘                    │
└──────────────────────────────────────────────────────────────────┘
```

### Django App Structure

```
sikika/
├── manage.py
├── requirements.txt
├── sikika/                    # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py               # ASGI for WebSocket support
│   └── wsgi.py
├── core/                      # Main application
│   ├── models.py             # All data models
│   ├── views.py              # HTTP views
│   ├── consumers.py          # WebSocket consumers (Django Channels)
│   ├── routing.py            # WebSocket URL routing
│   ├── urls.py               # HTTP URL routing
│   ├── forms.py              # Django forms
│   ├── admin.py              # Admin customization
│   ├── glossary_data.py      # Pre-seeded technical term glossary
│   └── slide_processor.py    # Slide description generator
├── templates/
│   ├── base.html             # Accessible base template
│   ├── home.html             # Landing page
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── lecturer/
│   │   ├── dashboard.html    # Lecturer main view
│   │   ├── session.html      # Live session control
│   │   └── history.html      # Past sessions
│   └── student/
│       ├── join.html         # Enter session code
│       ├── caption_mode.html # Live caption view
│       ├── audio_mode.html   # Audio description view
│       ├── sign_mode.html    # Sign language view
│       └── transcript.html   # Post-session transcript
├── static/
│   ├── css/
│   │   ├── main.css          # Core styles
│   │   ├── accessibility.css  # High contrast, dyslexia font, etc.
│   │   └── captions.css      # Caption-specific styles
│   ├── js/
│   │   ├── speech_capture.js  # Web Speech API (lecturer side)
│   │   ├── websocket.js       # WebSocket connection management
│   │   ├── captions.js        # Caption rendering + auto-scroll
│   │   ├── audio_desc.js      # Text-to-speech for blind mode
│   │   ├── sign_display.js    # Sign language animation display
│   │   └── accessibility.js   # Font size, contrast, preferences
│   └── signs/                 # Sign language GIF library
│       ├── common/
│       └── technical/
└── media/
    └── slides/                # Uploaded lecture slides
```

---

## 6. Data Models

### User Model (extends Django User)

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    role = models.CharField(choices=['lecturer', 'student'])
    university = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    
    # Accessibility preferences (students)
    preferred_mode = models.CharField(choices=[
        'caption', 'audio', 'sign'
    ], default='caption')
    font_size = models.CharField(choices=[
        'small', 'medium', 'large', 'extra-large'
    ], default='medium')
    high_contrast = models.BooleanField(default=False)
    dyslexia_font = models.BooleanField(default=False)
    caption_language = models.CharField(default='en')
```

### Session Model

```python
class LectureSession(models.Model):
    lecturer = models.ForeignKey(User)
    title = models.CharField(max_length=300)       # e.g., "Database Systems - Lecture 7"
    course_name = models.CharField(max_length=200)  # e.g., "Database Systems"
    join_code = models.CharField(max_length=6, unique=True)  # e.g., "XK47"
    status = models.CharField(choices=[
        'waiting', 'live', 'ended'
    ], default='waiting')
    started_at = models.DateTimeField(null=True)
    ended_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Transcript Model

```python
class TranscriptSegment(models.Model):
    session = models.ForeignKey(LectureSession)
    text = models.TextField()                       # The transcribed text
    timestamp = models.FloatField()                 # Seconds from session start
    has_technical_terms = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Slide Model

```python
class SessionSlide(models.Model):
    session = models.ForeignKey(LectureSession)
    slide_number = models.IntegerField()
    image = models.ImageField(upload_to='slides/')
    ai_description = models.TextField(blank=True)   # AI-generated description for blind students
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

### Glossary Model

```python
class GlossaryTerm(models.Model):
    term = models.CharField(max_length=200)
    definition = models.TextField()                  # Plain language definition
    subject_area = models.CharField(max_length=100)  # e.g., "Computer Science", "Biology"
    sign_animation = models.FileField(null=True)     # GIF/video of sign for this term
```

### Session Attendance

```python
class SessionAttendance(models.Model):
    session = models.ForeignKey(LectureSession)
    student = models.ForeignKey(User)
    mode_used = models.CharField(choices=[
        'caption', 'audio', 'sign'
    ])
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True)
```

---

## 7. Feature Specifications

### 7.1 Lecturer Panel

#### Create Session
- Lecturer logs in → clicks "New Session"
- Fills in: Session title, Course name
- System generates a unique 4-character join code (alphanumeric, uppercase)
- Session created in "waiting" status

#### Start Live Session
- Lecturer clicks "Start Live Session"
- Browser requests microphone permission
- Web Speech API begins continuous recognition
- Status changes to "live"
- WebSocket connection established with server
- Real-time transcript segments are sent to server every ~2-3 seconds

#### Slide Management
- Lecturer can upload slides (images or PDF) before or during session
- Slides are processed for AI descriptions (for blind students)
- Lecturer can advance slides manually, triggering description broadcast to audio mode students
- For hackathon: descriptions are pre-generated; system shows the flow

#### Session Dashboard (During Live Session)
- Shows session title, join code, duration timer
- Connected students count, broken down by mode:
  - 🔤 Caption mode: X students
  - 🔊 Audio mode: X students
  - 🤟 Sign mode: X students
- Live transcript feed (what the students are seeing)
- Slide controls (prev/next)

#### End Session
- Lecturer clicks "End Session"
- Full transcript is compiled and saved
- Session status → "ended"
- All connected students are notified
- Transcript available for download

### 7.2 Student — Caption Mode

#### Join Session
- Student enters 4-character code on join page
- Selects "Caption Mode"
- WebSocket connection established
- Accessibility preferences loaded (font size, contrast, etc.)

#### Live Caption View
- Full-screen caption display optimized for readability
- Text appears in real-time as the lecturer speaks
- **Auto-scroll**: New text appears at the bottom, previous text scrolls up
- **Pause scroll**: Student can tap to pause auto-scroll and read back
- **Resume**: Tap again to jump to current position

#### Smart Features
- **Technical term detection**: Terms from the glossary are highlighted with a different color
- **Inline definitions**: Tapping a highlighted term shows a plain-language definition
- **Paragraph grouping**: Text is grouped into natural paragraphs (by pauses) for readability

#### Accessibility Controls
- **Font size**: Small / Medium / Large / Extra Large (buttons always visible)
- **High contrast**: Toggle white-on-black mode
- **Dyslexia-friendly font**: Toggle OpenDyslexic font
- **Caption language**: Switch display language (for future multi-language support)

#### Post-Session
- Full transcript available to read and download
- Technical terms glossary from this session
- Time-stamped for easy reference

### 7.3 Student — Audio Description Mode

#### Join Session
- Student enters code, selects "Audio Mode"
- System confirms: "You'll hear slide descriptions through your device speaker or earphones. Plug in earphones for best experience."

#### During Session
- When lecturer advances to a new slide:
  - The slide's AI-generated description is displayed on screen as text
  - Browser's Speech Synthesis API reads the description aloud
  - Student can: pause, adjust volume, adjust speed (0.5x to 2x)
  
- Between slides: screen shows a simple status indicator
  - "Listening... Slide 4 of 20 — Entity Relationship Diagrams"
  
- Text version of all slide descriptions is listed below (scrollable)

#### Controls
- ⏸ Pause / ▶ Play
- 🔊 Volume control
- 🐌 Speed control (0.5x — 1x — 1.5x — 2x)
- Font size for the text version

#### Post-Session
- All slide descriptions downloadable as a document
- Combined with transcript for a complete lecture record

### 7.4 Student — Sign Language Mode (Prototype)

#### What It Shows
- Split screen:
  - **Left/Top**: Live captions (same as caption mode)
  - **Right/Bottom**: Sign language visual panel
  
- When a recognized term appears in the captions, the corresponding sign language animation (GIF) plays in the sign panel
- For the hackathon: we pre-load ~30-50 common academic/technical signs

#### Honest Scope
- This is a **prototype** demonstrating the concept
- Full 3D avatar-based continuous sign language is on the post-hackathon roadmap
- The captioning portion works fully; the sign animations enhance key terms

### 7.5 Landing Page

#### Layout
```
┌───────────────────────────────────────────┐
│           🤟 SIKIKA                        │
│        "To Be Heard"                       │
│                                            │
│  Real-time lecture accessibility for       │
│  deaf and blind university students.       │
│  No interpreters. No special hardware.     │
│  Just open your browser.                   │
│                                            │
│  [I'm a Lecturer]    [I'm a Student]      │
│                                            │
│  ─── HOW IT WORKS ───                     │
│                                            │
│  1. 🎙️ Lecturer starts a session          │
│  2. 📱 Students join with a code          │
│  3. 🔤 AI delivers live captions,         │
│     audio descriptions, and sign language  │
│                                            │
│  ─── IMPACT ───                           │
│                                            │
│  • Replaces $50K+/year interpreter costs  │
│  • Works on any device with a browser     │
│  • Supports multiple accessibility modes   │
│  • Full lecture transcripts, automatically │
│                                            │
│  [Watch Demo Video]  [Learn More]         │
└───────────────────────────────────────────┘
```

---

## 8. Tech Stack

| Component | Technology | Why |
|---|---|---|
| **Backend** | Django 5.x | Robust, fast development, built-in auth/admin, Python ecosystem |
| **Real-time** | Django Channels + WebSockets | Enables live bidirectional communication between lecturer and students |
| **ASGI Server** | Daphne | Required for Django Channels WebSocket support |
| **Database** | SQLite (hackathon) | Zero config, good enough for demo. PostgreSQL for production. |
| **Speech-to-Text** | Web Speech API (browser) | FREE, real-time, no API key, supports multiple languages |
| **Text-to-Speech** | Web Speech Synthesis API (browser) | FREE, built into all modern browsers |
| **Frontend** | HTML + CSS + Bootstrap 5 + Vanilla JS | Fast to build, responsive, accessible out of the box |
| **Accessibility CSS** | Custom + OpenDyslexic font | High contrast, font sizing, dyslexia support |
| **Channel Layer** | In-memory (hackathon) | Redis for production. In-memory works for demo. |

### Key Dependencies (requirements.txt)

```
django>=5.0
channels>=4.0
daphne>=4.0
Pillow>=10.0          # Image handling for slides
```

---

## 9. 48-Hour Build Plan

### Phase 1: Foundation (Hours 0–3)

**Goal**: Django project running, models created, auth working, base template ready.

- [ ] Create Django project with `channels` configured
- [ ] Set up ASGI with Daphne
- [ ] Define all models (UserProfile, LectureSession, TranscriptSegment, SessionSlide, GlossaryTerm, SessionAttendance)
- [ ] Run migrations
- [ ] Create registration + login views (lecturer and student roles)
- [ ] Build accessible base template:
  - Bootstrap 5 with responsive layout
  - CSS variables for font size and contrast
  - Skip-to-content links, ARIA labels, semantic HTML
  - OpenDyslexic font loaded
- [ ] Create basic navigation (role-based: lecturer vs student)

### Phase 2: WebSocket Infrastructure (Hours 3–8)

**Goal**: Real-time communication pipe works.

- [ ] Configure Django Channels with in-memory channel layer
- [ ] Create `LectureConsumer` (WebSocket consumer):
  - `connect()`: Join session group
  - `receive()`: Accept transcript text from lecturer, broadcast to group
  - `disconnect()`: Leave session group
- [ ] Create routing for WebSocket URLs
- [ ] Build session creation view (lecturer creates session, gets join code)
- [ ] Build session join view (student enters code, joins WebSocket group)
- [ ] Test: Lecturer sends a text message → all connected students receive it in real-time
- **Milestone**: Real-time text broadcasting works end-to-end

### Phase 3: Live Transcription (Hours 8–14)

**Goal**: Lecturer speaks → students see live text.

- [ ] Build `speech_capture.js`:
  - Initialize Web Speech API (`webkitSpeechRecognition`)
  - Continuous recognition mode
  - `onresult` callback sends transcript text via WebSocket
  - Handle interim vs final results (show interim for responsiveness)
  - Auto-restart on recognition end (continuous listening)
  - Language selection support
- [ ] Build lecturer session page:
  - Start/stop button
  - Live preview of what's being captured
  - Session info (code, connected count)
  - Microphone status indicator
- [ ] Build `captions.js`:
  - Receive WebSocket messages
  - Render text with smooth animations
  - Auto-scroll behavior
  - Pause/resume scroll
- [ ] Build basic caption mode student page:
  - Clean, full-screen caption display
  - Connection status indicator
- **Milestone**: Lecturer speaks into mic → student on another device sees live text

### Phase 4: Smart Captions (Hours 14–22)

**Goal**: Captions are intelligent, accessible, and beautiful.

- [ ] Seed glossary data:
  - 50+ Computer Science terms (for demo)
  - 30+ general academic terms
  - Each with plain-language definition
- [ ] Build term detection in `captions.js`:
  - Match incoming text against glossary
  - Wrap matched terms in highlighted spans
  - On tap/hover: show definition tooltip/popup
- [ ] Build accessibility controls:
  - Font size buttons (S / M / L / XL) — live update
  - High contrast toggle (CSS class swap)
  - Dyslexia font toggle (CSS class swap)
  - Persist preferences in localStorage + user profile
- [ ] Style the caption view:
  - Clean, distraction-free UI
  - Smooth text appearance animation
  - Current text highlighted, older text faded slightly
  - Mobile-responsive (works on phone screen)
- [ ] Build transcript save:
  - All segments saved to database with timestamps
  - Download button: export as .txt file
- **Milestone**: Beautiful, smart, accessible live captions working perfectly

### Phase 5: Audio Description (Hours 22–30)

**Goal**: Blind students hear slide descriptions.

- [ ] Build slide upload for lecturers:
  - Upload images or PDF (converted to images)
  - Reorder slides
  - Add/edit text descriptions manually
  - AI auto-generate descriptions (using a simple image description — for hackathon: pre-written descriptions demonstrated with real flow)
- [ ] Build slide advancement:
  - Lecturer clicks Next/Prev
  - Server broadcasts current slide number to all connected students
- [ ] Build `audio_desc.js`:
  - On receiving slide change event:
    - Fetch slide description
    - Use Speech Synthesis API to read it aloud
    - Show text version on screen simultaneously
  - Controls: pause, speed, volume
- [ ] Build audio mode student page:
  - Current slide info
  - Audio controls
  - Text list of all slide descriptions
  - Accessible: keyboard navigable, screen-reader compatible
- **Milestone**: Lecturer advances slide → blind student's phone reads the description aloud

### Phase 6: Sign Language Prototype (Hours 30–34)

**Goal**: Demonstrate sign language concept.

- [ ] Collect/create 30-50 sign language GIFs for common academic terms
  - Source from open sign language databases (ASL/KSL)
  - Focus on terms that appear in the demo
- [ ] Build `sign_display.js`:
  - Monitor incoming caption text for glossary matches
  - When a matched term appears, display corresponding sign GIF
  - Smooth transition between signs
- [ ] Build sign mode student page:
  - Split layout: captions on top/left, sign animation on bottom/right
  - Sign animation panel with term label
  - Full caption functionality underneath
- **Milestone**: As lecturer speaks, relevant sign language GIFs appear alongside captions

### Phase 7: Lecturer Dashboard + Landing (Hours 34–38)

**Goal**: Lecturer side complete, landing page live.

- [ ] Build lecturer dashboard:
  - Create new session
  - View past sessions
  - Session stats (students served, modes used, duration)
- [ ] Build post-session view:
  - Full transcript
  - Attendance log
  - Download transcript
- [ ] Build landing page:
  - Hero section with tagline
  - How it works (3 steps)
  - Impact stats (seeded)
  - "I'm a Lecturer" / "I'm a Student" buttons
  - Fully accessible, beautiful design
- **Milestone**: Complete user journey from landing → session → post-session

### Phase 8: Polish + Demo Prep (Hours 38–48)

**Goal**: Everything is beautiful, bug-free, and demo-ready.

- [ ] UI polish:
  - Consistent spacing, colors, typography
  - Loading states and error handling
  - Mobile responsiveness check
  - All accessibility features tested
- [ ] Seed demo data:
  - Demo lecturer account with past sessions
  - Sample transcript data
  - 15-20 slide images with descriptions (for a "Database Systems" demo lecture)
  - Glossary populated for the demo subject
- [ ] Bug fixes and edge cases:
  - WebSocket reconnection on drop
  - Handle speech recognition errors gracefully
  - Handle slow connections
- [ ] Prepare demo flow:
  - Laptop 1: Lecturer starts session
  - Laptop/Phone 2: Student in caption mode
  - Phone 3: Student in audio mode
  - Phone 4 (if available): Student in sign mode
  - Pre-plan what the lecturer will say during the demo
- [ ] Prepare pitch:
  - The Problem (30 seconds)
  - The Solution (60 seconds)
  - Live Demo (3-4 minutes)
  - Impact & Vision (60 seconds)
  - Q&A prep: anticipate judge questions

---

## 10. Demo Script

### Setup (before going on stage)
- Lecturer device: browser open to SIKIKA, session created
- Student devices: ready to join
- Have earphones connected to "blind student" phone

### The Demo (5 minutes)

**[0:00 — The Problem]**
"In African universities, deaf students depend on sign language interpreters who are scarce, expensive, and lose 30% of content. Blind students get materials days late. SIKIKA changes this."

**[0:30 — Start Session]**
*Lecturer device*: "I create a session — Database Systems Lecture 7. Session code: XK47."

**[0:45 — Students Join]**
*Three student devices*: "Three students join. One chooses captions. One chooses audio descriptions. One chooses sign language mode."

**[1:00 — Live Captioning Demo]**
*Start speaking into lecturer device*: "Today we're going to discuss database normalization. Normalization is the process of organizing data to reduce redundancy..."

*Show student caption device*: "Watch — the captions appear in real-time. Notice how 'normalization' and 'redundancy' are highlighted. Tap 'normalization'..." *tap* "...and you get an instant plain-language definition."

**[2:00 — Accessibility Controls]**
"This student needs larger text." *Increase font size.* "This student needs high contrast." *Toggle.* "Every student controls their own experience."

**[2:30 — Audio Description Demo]**
"Now I advance to a slide showing an ER diagram."
*Advance slide on lecturer device.*
*Hold up 'blind student' phone with earphone*: "Listen — the phone is describing the diagram: 'The slide shows three tables: Students, Courses, and Enrollments, connected by one-to-many relationships.'"

**[3:15 — Sign Language Demo]**
*Show sign mode device*: "As I speak, relevant sign language animations appear alongside the captions for key terms."

**[3:45 — Post-Session Value]**
*End session.* "When the lecture ends, every student gets the full, searchable transcript with all technical terms defined. No more missed lectures. No more falling behind."

**[4:15 — The Impact]**
"SIKIKA replaces $50,000+/year in interpreter costs with a free, browser-based solution. It requires zero hardware, zero installs. Any lecturer, any classroom, any student — just open your browser."

**[4:45 — Close]**
"15% of the world's population has a disability. In African universities, they're being left behind — not because we don't care, but because the current solutions don't scale. SIKIKA makes every lecture accessible to every student. Thank you."

---

## 11. Addressing the Problem Statements

The hackathon gave us:

| Problem Statement | How SIKIKA Addresses It |
|---|---|
| **"Develop a digital solution that enhances learning, teaching, and academic management in higher education institutions"** | SIKIKA enhances LEARNING by making lectures accessible in real-time. It enhances TEACHING by giving lecturers a frictionless way to make their content accessible. It enhances ACADEMIC MANAGEMENT by providing inclusion metrics and compliance data. |
| **"Develop a solution that ensures equitable access to quality learning for students of all abilities and backgrounds"** | This IS our core mission. Deaf students get captions. Blind students get audio descriptions. Language-diverse students get translation. Economic barriers removed (free, browser-based). |
| **"Microcredentials are a way for students to do courses relevant to their degree"** | The transcript + glossary system creates automatic study materials from every lecture. These are stackable, reusable, and can be structured as micro-learning units. Post-hackathon: formal microcredentials in accessibility and inclusive teaching for lecturers. |
| **"Develop a platform that enables university students to access industry-relevant microcredential courses"** | SIKIKA's accessibility engine can be applied beyond the classroom — to online courses, webinars, industry workshops — making ALL learning industry-relevant learning accessible. The platform becomes infrastructure for inclusive learning of any kind. |

---

## 12. Uniqueness Defense

### "Isn't this just Google's Live Transcribe?"
Google Live Transcribe is a **personal** app that transcribes ambient audio on ONE phone. It:
- Has no concept of a classroom session
- Doesn't share between lecturer and multiple students
- Doesn't detect or define technical terms
- Doesn't describe slides for blind students
- Doesn't save searchable transcripts
- Doesn't provide sign language
- Isn't designed for education at all

### "Isn't this like Otter.ai?"
Otter.ai records and transcribes meetings. It:
- Is designed for business meetings, not university lectures
- Costs $16.99/month per user
- Doesn't provide real-time broadcast to multiple students
- Has no accessibility modes (sign language, audio descriptions)
- Has no educational intelligence (term detection, definitions)
- Doesn't work offline-capable or for low-bandwidth African contexts

### "Can't students just use ChatGPT?"
ChatGPT:
- Cannot hear a live lecture in real-time
- Cannot broadcast to 100+ students simultaneously
- Cannot describe slides being shown on a projector
- Cannot provide sign language visuals
- Requires the student to already know what they missed (but they don't know what they don't know)

### "What about Microsoft's real-time captions in Teams/PowerPoint?"
- Requires Microsoft Teams or PowerPoint (not every lecturer uses them)
- In-person lectures are NOT Teams meetings
- No sign language mode
- No educational term intelligence
- No slide description for blind students
- Not designed for the African university context (connectivity, devices)

---

## 13. Pitch Talking Points

### For Judges — What to Emphasize

1. **Scale of problem**: 15% of global population has disabilities. Interpreter supply is mathematically impossible to scale. This is not a niche — it's hundreds of millions of people.

2. **Zero cost to deploy**: No hardware, no app install, no paid API. A university can start using SIKIKA in 5 minutes.

3. **Cost SAVINGS**: We don't add cost — we REMOVE it. A university paying $50K+/year for interpreters can replace that with a free browser-based solution.

4. **Live demo is undeniable**: The judge SEES it work in real-time. Someone speaks → text appears on another device → terms are defined → slides are described aloud. You can't argue with a working demo.

5. **Beyond disability**: Every student benefits from searchable lecture transcripts. International students benefit from language translation. This isn't "just for disabled students" — it's universal design that serves everyone.

6. **Regulatory tailwind**: Universities are increasingly REQUIRED to provide accessibility. SIKIKA gives them a way to actually comply.

### Anticipated Judge Questions

| Question | Answer |
|---|---|
| "What about noisy classrooms?" | The lecturer's device mic is close to them. Web Speech API handles background noise well. For production: dedicated lapel mic. |
| "What about internet connectivity?" | The system is lightweight — only text is transmitted (a few KB). Works on 2G+ connections. |
| "What about accuracy?" | Web Speech API is 95%+ accurate for clear English. The smart term detection adds another layer of clarity. |
| "What about other languages?" | Web Speech API supports 60+ languages including French, Swahili, Arabic. We demo in English but the system is multilingual. |
| "How do you make money?" | University licensing ($2-5/student/month) — still 90% cheaper than human interpreters. Free tier for individual students. |
| "What's the competitive moat?" | First-mover in African university accessibility + the educational intelligence layer (glossary, term detection, session management) that generic transcription tools don't have. |

---

*End of Hackathon Build Document*
