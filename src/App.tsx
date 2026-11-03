
import { useEffect, useState } from 'react'
import ListeningPage from './pages/ListeningPage'
import SpeakingPage from './pages/SpeakingPage'
import './App.css'

// ======================================
// TYPES
// ======================================

type WordResult = {
  word: string
  category: string
  japanese?: string
  definition?: string
  confidence: number
  review_required: boolean
  level?: string
}

type AnalysisData = {
  total_words: number
  review_count: number
  results: WordResult[]
}

type SavedWord = WordResult & {
  savedAt: string
  sourceSentence: string
}

type FilterType = 'all' | 'academic' | 'general' | 'review'

type PageType =
  | 'dashboard'
  | 'vocabulary'
  | 'review'
  | 'progress'
  | 'writing'
  | 'listening'
  | 'speaking'
  | 'settings'

// ======================================
// STORAGE
// ======================================

const STORAGE_KEYS = {
  saved: 'academia_saved_words',
  mastered: 'academia_mastered_words',
  practice: 'academia_practice_words',
  history: 'academia_study_history',
  language: 'academia_interface_language',
}

function loadStorage<T>(key: string, fallback: T): T {
  try {
    const stored = localStorage.getItem(key)
    return stored ? (JSON.parse(stored) as T) : fallback
  } catch {
    return fallback
  }
}

// ======================================
// CONSTANTS
// ======================================



// ======================================
// MAIN APP
// ======================================

function App() {
  // ----------------------------------
  // ANALYZER STATE
  // ----------------------------------

  const [text, setText] = useState('')
  const [analyzedText, setAnalyzedText] = useState('')
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // ----------------------------------
  // WRITING STATE
  // ----------------------------------

  const [writingText, setWritingText] = useState('')
  const [writingLoading, setWritingLoading] = useState(false)
  const [writingError, setWritingError] = useState('')
  const [writingResult, setWritingResult] =
    useState<AnalysisData | null>(null)

  // ----------------------------------
  // LEARNING DATA
  // ----------------------------------

  const [savedWords, setSavedWords] = useState<SavedWord[]>(
    () => loadStorage<SavedWord[]>(STORAGE_KEYS.saved, [])
  )

  const [masteredWords, setMasteredWords] = useState<string[]>(
    () => loadStorage<string[]>(STORAGE_KEYS.mastered, [])
  )

  const [practiceWords, setPracticeWords] = useState<string[]>(
    () => loadStorage<string[]>(STORAGE_KEYS.practice, [])
  )

  const [studyHistory, setStudyHistory] = useState<string[]>(
    () => loadStorage<string[]>(STORAGE_KEYS.history, [])
  )

  // ----------------------------------
  // NAVIGATION STATE
  // ----------------------------------

  const [currentPage, setCurrentPage] =
    useState<PageType>('dashboard')

  const [filter, setFilter] = useState<FilterType>('all')
  const [selectedWord, setSelectedWord] = useState<string | null>(null)
  const [reviewIndex, setReviewIndex] = useState(0)
  const [showAnswer, setShowAnswer] = useState(false)
  const [reviewFeedback, setReviewFeedback] = useState('')

  // ----------------------------------
  // SETTINGS STATE
  // ----------------------------------

  const [interfaceLanguage, setInterfaceLanguage] =
    useState<'EN' | 'JP'>(
      () => loadStorage<'EN' | 'JP'>(
        STORAGE_KEYS.language,
        'EN'
      )
    )

  // ======================================
  // SAVE DATA AUTOMATICALLY
  // ======================================

  useEffect(() => {
    localStorage.setItem(
      STORAGE_KEYS.saved,
      JSON.stringify(savedWords)
    )
  }, [savedWords])

  useEffect(() => {
    localStorage.setItem(
      STORAGE_KEYS.mastered,
      JSON.stringify(masteredWords)
    )
  }, [masteredWords])

  useEffect(() => {
    localStorage.setItem(
      STORAGE_KEYS.practice,
      JSON.stringify(practiceWords)
    )
  }, [practiceWords])

  useEffect(() => {
    localStorage.setItem(
      STORAGE_KEYS.history,
      JSON.stringify(studyHistory)
    )
  }, [studyHistory])

  useEffect(() => {
    localStorage.setItem(
      STORAGE_KEYS.language,
      JSON.stringify(interfaceLanguage)
    )
  }, [interfaceLanguage])

  // ======================================
  // LEARNING HISTORY
  // ======================================

  function recordStudySession() {
    const now = new Date()

    const year = now.getFullYear()
    const month = String(now.getMonth() + 1).padStart(2, '0')
    const date = String(now.getDate()).padStart(2, '0')

    const today = `${year}-${month}-${date}`

    setStudyHistory((previous) =>
      previous.includes(today)
        ? previous
        : [...previous, today]
    )
  }

  // ======================================
  // SOURCE SENTENCE
  // ======================================

  function getSourceSentence(sourceText: string, word: string) {
    const escapedWord = word.replace(
      /[.*+?^${}()|[\]\\]/g,
      '\\$&'
    )

    return (
      sourceText
        .split(/(?<=[.!?])\s+/)
        .find((sentence) =>
          new RegExp(`\\b${escapedWord}\\b`, 'i').test(sentence)
        ) || 'Original sentence not found.'
    )
  }

  // ======================================
  // API REQUEST
  // ======================================

  async function requestAnalysis(
    inputText: string
  ): Promise<AnalysisData> {
    const response = await fetch(
      'http://127.0.0.1:8000/analyze',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      }
    )

    if (!response.ok) {
      throw new Error('Analysis failed.')
    }

    const data: AnalysisData = await response.json()

    if (!Array.isArray(data.results)) {
      throw new Error('Invalid analysis response.')
    }

    return data
  }

  // ======================================
  // VOCABULARY ANALYSIS
  // ======================================

  async function handleAnalyze() {
    if (!text.trim()) {
      setError('Please enter an English text.')
      return
    }

    setLoading(true)
    setError('')
    setAnalysis(null)
    setFilter('all')
    setSelectedWord(null)

    try {
      const data = await requestAnalysis(text)

      setAnalysis(data)
      setAnalyzedText(text)
      recordStudySession()
    } catch {
      setError(
        'Could not connect to ACADEMIA. Check that the API is running.'
      )
    } finally {
      setLoading(false)
    }
  }

  // ======================================
  // WRITING ANALYSIS
  // ======================================

  async function handleWritingAnalysis() {
    if (!writingText.trim()) {
      setWritingError('Please enter your writing.')
      return
    }

    setWritingLoading(true)
    setWritingError('')
    setWritingResult(null)

    try {
      const data = await requestAnalysis(writingText)

      setWritingResult(data)
      recordStudySession()
    } catch {
      setWritingError(
        'Could not connect to ACADEMIA. Check that the API is running.'
      )
    } finally {
      setWritingLoading(false)
    }
  }

  // ======================================
  // VOCABULARY FUNCTIONS
  // ======================================

  function isSaved(word: string) {
    return savedWords.some(
      (item) => item.word.toLowerCase() === word.toLowerCase()
    )
  }

  function toggleSaveWord(item: WordResult) {
    if (isSaved(item.word)) {
      removeSavedWord(item.word)
      return
    }

    setSavedWords((previous) => [
      ...previous,
      {
        ...item,
        savedAt: new Date().toISOString(),
        sourceSentence: getSourceSentence(
          analyzedText,
          item.word
        ),
      },
    ])

    recordStudySession()
  }

  function removeSavedWord(word: string) {
    const normalized = word.toLowerCase()

    setSavedWords((previous) =>
      previous.filter(
        (item) => item.word.toLowerCase() !== normalized
      )
    )

    setMasteredWords((previous) =>
      previous.filter(
        (item) => item.toLowerCase() !== normalized
      )
    )

    setPracticeWords((previous) =>
      previous.filter(
        (item) => item.toLowerCase() !== normalized
      )
    )

    setReviewIndex(0)
    setShowAnswer(false)
    setReviewFeedback('')
  }

  function markWordAsMastered(word: string) {
    setMasteredWords((previous) =>
      previous.includes(word)
        ? previous
        : [...previous, word]
    )

    setPracticeWords((previous) =>
      previous.filter((item) => item !== word)
    )

    setReviewFeedback(`✓ "${word}" marked as mastered!`)
    recordStudySession()

    if (savedWords.length > 1) {
      goToNextWord()
    }
  }

  function markWordForPractice(word: string) {
    setPracticeWords((previous) =>
      previous.includes(word)
        ? previous
        : [...previous, word]
    )

    setMasteredWords((previous) =>
      previous.filter((item) => item !== word)
    )

    setReviewFeedback(`↻ "${word}" added to your practice list.`)
    recordStudySession()
  }

  // ======================================
  // REVIEW FUNCTIONS
  // ======================================

  function startReview() {
    setCurrentPage('review')
    setReviewIndex(0)
    setShowAnswer(false)
    setReviewFeedback('')
  }

  function goToNextWord() {
    if (savedWords.length === 0) return

    setReviewIndex((previous) =>
      previous >= savedWords.length - 1
        ? 0
        : previous + 1
    )

    setShowAnswer(false)
  }

  function goToPreviousWord() {
    setReviewIndex((previous) => Math.max(0, previous - 1))
    setShowAnswer(false)
  }

  // ======================================
  // ANALYSIS DATA
  // ======================================

  const results = analysis?.results ?? []

  const academicCount = results.filter((item) =>
    item.category.toLowerCase().includes('academic')
  ).length

  const generalCount = results.filter((item) =>
    item.category.toLowerCase().includes('general')
  ).length

  const reviewCount = results.filter(
    (item) =>
      item.review_required ||
      item.category.toLowerCase().includes('review')
  ).length

  const filteredResults = results.filter((item) => {
    if (filter === 'academic') {
      return item.category.toLowerCase().includes('academic')
    }

    if (filter === 'general') {
      return item.category.toLowerCase().includes('general')
    }

    if (filter === 'review') {
      return (
        item.review_required ||
        item.category.toLowerCase().includes('review')
      )
    }

    return true
  })

  const validMasteredCount = savedWords.filter((item) =>
    masteredWords.includes(item.word)
  ).length

  const masteryRate =
    savedWords.length === 0
      ? 0
      : Math.round(
          (validMasteredCount / savedWords.length) * 100
        )

  const currentReviewWord =
    savedWords.length > 0
      ? savedWords[reviewIndex % savedWords.length]
      : undefined

  // ======================================
  // WEEKLY STUDY DAYS
  // ======================================

  const today = new Date()
  const day = today.getDay()
  const mondayOffset = day === 0 ? 6 : day - 1

  const monday = new Date(today)
  monday.setDate(today.getDate() - mondayOffset)
  monday.setHours(0, 0, 0, 0)

  const weeklyStudyDays = studyHistory.filter(
    (date) => new Date(`${date}T12:00:00`) >= monday
  ).length

  // ======================================
  // STYLES
  // ======================================

  const filterButtonStyle = (selected: boolean) => ({
    padding: '9px 16px',
    borderRadius: '8px',
    border: selected
      ? '1px solid #356AE6'
      : '1px solid #E2E8F0',
    background: selected ? '#EAF1FF' : '#FFFFFF',
    color: selected ? '#356AE6' : '#64748B',
    fontWeight: selected ? 600 : 500,
    cursor: 'pointer' as const,
  })

  const summaryCardStyle = {
    padding: '18px',
    border: '1px solid #E2E8F0',
    borderRadius: '12px',
    background: '#FFFFFF',
  }

  const primaryButtonStyle = {
    padding: '10px 16px',
    border: 'none',
    borderRadius: '8px',
    background: '#356AE6',
    color: '#FFFFFF',
    cursor: 'pointer',
    fontWeight: 600,
  }

  const pageTitles: Record<PageType, string> = {
    dashboard: 'Dashboard',
    vocabulary: 'My Vocabulary',
    review: 'Review Mode',
    progress: 'Learning Progress',
    writing: 'Writing Analyzer',
    listening: 'Listening',
    speaking: 'Speaking',
    settings: 'Settings',
  }

  // ======================================
  // PAGE
  // ======================================

  return (
    <div className="app">

      {/* SIDEBAR */}

      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">A</div>
          <div>
            <h1>ACADEMIA</h1>
            <span>Academic English</span>
          </div>
        </div>

        <nav className="navigation">

          <p className="nav-label">LEARNING</p>

          <button
            className={`nav-item ${currentPage === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentPage('dashboard')}
          >
            <span>▦</span> Dashboard
          </button>

          <button
            className={`nav-item ${currentPage === 'vocabulary' ? 'active' : ''}`}
            onClick={() => setCurrentPage('vocabulary')}
          >
            <span>📖</span> My Vocabulary
          </button>

          <button
            className={`nav-item ${currentPage === 'review' ? 'active' : ''}`}
            onClick={startReview}
          >
            <span>✎</span> Review Mode
          </button>

          <button
            className={`nav-item ${currentPage === 'progress' ? 'active' : ''}`}
            onClick={() => setCurrentPage('progress')}
          >
            <span>▥</span> Learning Progress
          </button>

          <p className="nav-label second-label">
            SKILL DEVELOPMENT
          </p>

          <button
            className={`nav-item ${currentPage === 'writing' ? 'active' : ''}`}
            onClick={() => setCurrentPage('writing')}
          >
            <span>▤</span> Writing Analyzer
          </button>

          <button
            className={`nav-item ${currentPage === 'listening' ? 'active' : ''}`}
            onClick={() => setCurrentPage('listening')}
          >
            <span>◉</span> Listening
          </button>

          <button
            className={`nav-item ${currentPage === 'speaking' ? 'active' : ''}`}
            onClick={() => setCurrentPage('speaking')}
          >
            <span>◎</span> Speaking
          </button>

          <p className="nav-label second-label">SETTINGS</p>

          <button
            className={`nav-item ${currentPage === 'settings' ? 'active' : ''}`}
            onClick={() => setCurrentPage('settings')}
          >
            <span>⚙</span> Settings
          </button>

        </nav>

        <div className="sidebar-bottom">
          <div className="upgrade-card">
            <strong>Keep growing.</strong>
            <p>
              Build your academic English skills every day.
            </p>
          </div>

          <span className="version">
            ACADEMIA · BETA
          </span>
        </div>

      </aside>

      {/* MAIN CONTENT */}

      <main className="main-content">

        <header className="topbar">
          <div className="breadcrumb">
            Learning / {pageTitles[currentPage]}
          </div>

          <div className="topbar-right">
            <button
              className="language-button"
              onClick={() => setCurrentPage('settings')}
            >
              {interfaceLanguage} / {interfaceLanguage === 'EN' ? 'JP' : 'EN'}
            </button>

            <div className="avatar">A</div>
          </div>
        </header>

        <div className="dashboard">

          {/* ================================= */}
          {/* DASHBOARD */}
          {/* ================================= */}

          {currentPage === 'dashboard' && (
            <>

              <section className="welcome">
                <div>
                  <p className="eyebrow">YOUR LEARNING SPACE</p>
                  <h2>Welcome back!</h2>
                  <p className="welcome-description">
                    Every step brings you closer to academic confidence.
                  </p>
                </div>
                <div className="welcome-decoration">A</div>
              </section>

              <section
                className="panel"
                style={{ marginBottom: '28px', padding: '24px' }}
              >
                <h3>ACADEMIA Vocabulary Analyzer</h3>
                <p>
                  Paste your academic English text and let ACADEMIA analyze it.
                </p>

                <textarea
                  value={text}
                  onChange={(event) => setText(event.target.value)}
                  placeholder="Paste your academic English paragraph here..."
                  rows={5}
                  style={{
                    width: '100%',
                    padding: '14px',
                    marginTop: '12px',
                    border: '1px solid #E2E8F0',
                    borderRadius: '10px',
                    fontSize: '15px',
                    resize: 'vertical',
                    boxSizing: 'border-box',
                  }}
                />

                <button
                  onClick={handleAnalyze}
                  disabled={loading || !text.trim()}
                  className="start-button"
                  style={{ marginTop: '12px' }}
                >
                  {loading ? 'Analyzing...' : 'Analyze my text →'}
                </button>

                {error && (
                  <p style={{ color: '#D94B4B', marginTop: '12px' }}>
                    {error}
                  </p>
                )}

                {analysis && (
                  <div style={{ marginTop: '28px' }}>
                    <h3>Analysis Results</h3>
                    <p style={{ color: '#64748B', marginTop: '6px' }}>
                      Your vocabulary breakdown
                    </p>

                    <div
                      style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                        gap: '14px',
                        marginTop: '20px',
                        marginBottom: '24px',
                      }}
                    >
                      <div style={summaryCardStyle}>
                        <p style={{ color: '#64748B', margin: 0 }}>
                          Total words
                        </p>
                        <strong style={{ fontSize: '28px' }}>
                          {analysis.total_words}
                        </strong>
                      </div>

                      <div style={summaryCardStyle}>
                        <p style={{ color: '#64748B', margin: 0 }}>
                          Academic Vocabulary
                        </p>
                        <strong style={{ fontSize: '28px', color: '#356AE6' }}>
                          {academicCount}
                        </strong>
                      </div>

                      <div style={summaryCardStyle}>
                        <p style={{ color: '#64748B', margin: 0 }}>
                          General Vocabulary
                        </p>
                        <strong style={{ fontSize: '28px' }}>
                          {generalCount}
                        </strong>
                      </div>

                      <div style={summaryCardStyle}>
                        <p style={{ color: '#64748B', margin: 0 }}>
                          Needs Review
                        </p>
                        <strong style={{ fontSize: '28px', color: '#D99525' }}>
                          {reviewCount}
                        </strong>
                      </div>
                    </div>

                    <h3 style={{ marginBottom: '12px' }}>
                      Vocabulary Categories
                    </h3>

                    <div
                      style={{
                        display: 'flex',
                        flexWrap: 'wrap',
                        gap: '8px',
                        marginBottom: '20px',
                      }}
                    >
                      <button
                        style={filterButtonStyle(filter === 'all')}
                        onClick={() => setFilter('all')}
                      >
                        All ({results.length})
                      </button>

                      <button
                        style={filterButtonStyle(filter === 'academic')}
                        onClick={() => setFilter('academic')}
                      >
                        Academic ({academicCount})
                      </button>

                      <button
                        style={filterButtonStyle(filter === 'general')}
                        onClick={() => setFilter('general')}
                      >
                        General ({generalCount})
                      </button>

                      <button
                        style={filterButtonStyle(filter === 'review')}
                        onClick={() => setFilter('review')}
                      >
                        Needs Review ({reviewCount})
                      </button>
                    </div>

                    {filteredResults.length === 0 ? (
                      <p style={{ color: '#64748B' }}>
                        No words found in this category.
                      </p>
                    ) : (
                      filteredResults.map((item, index) => {
                        const isSelected = selectedWord === item.word
                        const saved = isSaved(item.word)

                        return (
                          <div
                            key={`${item.word}-${index}`}
                            style={{
                              padding: '16px',
                              marginTop: '10px',
                              border: '1px solid #E2E8F0',
                              borderRadius: '10px',
                              background: '#FFFFFF',
                            }}
                          >
                            <div
                              style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                gap: '12px',
                                flexWrap: 'wrap',
                              }}
                            >
                              <strong style={{ fontSize: '17px' }}>
                                {item.word}
                              </strong>
                              <span style={{ color: '#356AE6' }}>
                                {item.category}
                              </span>
                            </div>

                            {item.japanese && (
                              <p style={{ margin: '8px 0' }}>
                                {item.japanese}
                              </p>
                            )}

                            {item.definition && (
                              <p style={{ color: '#64748B', margin: '8px 0' }}>
                                {item.definition}
                              </p>
                            )}

                            <small style={{ color: '#64748B' }}>
                              Confidence: {Math.round(item.confidence * 100)}%
                              {item.level ? ` · ${item.level}` : ''}
                              {item.review_required ? ' · Needs review' : ''}
                            </small>

                            <div
                              style={{
                                display: 'flex',
                                flexWrap: 'wrap',
                                gap: '8px',
                                marginTop: '12px',
                              }}
                            >
                              <button
                                onClick={() =>
                                  setSelectedWord(isSelected ? null : item.word)
                                }
                                style={filterButtonStyle(false)}
                              >
                                {isSelected ? 'Close details ↑' : 'View details →'}
                              </button>

                              <button
                                onClick={() => toggleSaveWord(item)}
                                style={{
                                  ...filterButtonStyle(saved),
                                  borderColor: saved ? '#16845B' : '#E2E8F0',
                                  background: saved ? '#E9F7F0' : '#FFFFFF',
                                  color: saved ? '#16845B' : '#64748B',
                                }}
                              >
                                {saved ? '✓ Saved' : '+ Save Word'}
                              </button>
                            </div>

                            {isSelected && (
                              <div
                                style={{
                                  marginTop: '14px',
                                  padding: '18px',
                                  background: '#F4F7FC',
                                  borderRadius: '10px',
                                  border: '1px solid #E2E8F0',
                                }}
                              >
                                <h4 style={{ marginTop: 0 }}>
                                  Word Details
                                </h4>

                                <p><strong>Word:</strong> {item.word}</p>
                                <p>
                                  <strong>Japanese Meaning:</strong>{' '}
                                  {item.japanese || 'Not available'}
                                </p>
                                <p>
                                  <strong>Academic Definition:</strong>{' '}
                                  {item.definition || 'Not available'}
                                </p>
                                <p>
                                  <strong>Word Level:</strong>{' '}
                                  {item.level || 'Not classified'}
                                </p>
                                <p>
                                  <strong>Category:</strong> {item.category}
                                </p>

                                <div
                                  style={{
                                    marginTop: '16px',
                                    padding: '14px',
                                    background: '#FFFFFF',
                                    borderRadius: '8px',
                                  }}
                                >
                                  <strong>Usage in Your Text</strong>
                                  <p style={{ color: '#64748B', lineHeight: 1.7 }}>
                                    {getSourceSentence(analyzedText, item.word)}
                                  </p>
                                </div>
                              </div>
                            )}
                          </div>
                        )
                      })
                    )}
                  </div>
                )}
              </section>

              <section className="section-heading">
                <div>
                  <h3>Your learning overview</h3>
                  <p>Track your progress and keep moving forward.</p>
                </div>
              </section>

              <section className="stats-grid">
                <article className="stat-card">
                  <span className="stat-icon">📚</span>
                  <p>Words Saved</p>
                  <strong>{savedWords.length}</strong>
                  <span className="stat-note">Your vocabulary collection</span>
                </article>

                <article className="stat-card">
                  <span className="stat-icon">🎓</span>
                  <p>Mastered Words</p>
                  <strong>{validMasteredCount}</strong>
                  <span className="stat-note">Words you have learned</span>
                </article>

                <article className="stat-card">
                  <span className="stat-icon">🎯</span>
                  <p>Need Practice</p>
                  <strong>{practiceWords.length}</strong>
                  <span className="stat-note">Words to review again</span>
                </article>
              </section>

              <section className="panel" style={{ padding: '24px', marginTop: '24px' }}>
                <h3>Learning Progress</h3>
                <p style={{ color: '#64748B' }}>
                  Your vocabulary learning progress
                </p>

                <div
                  style={{
                    height: '12px',
                    background: '#E2E8F0',
                    borderRadius: '20px',
                    overflow: 'hidden',
                    marginTop: '18px',
                  }}
                >
                  <div
                    style={{
                      height: '100%',
                      width: `${masteryRate}%`,
                      background: '#356AE6',
                      borderRadius: '20px',
                      transition: 'width 0.3s ease',
                    }}
                  />
                </div>

                <p style={{ marginTop: '12px' }}>
                  <strong>{masteryRate}%</strong> Mastery rate
                </p>

                <button
                  className="start-button"
                  onClick={() => setCurrentPage('progress')}
                >
                  View Learning Analytics →
                </button>
              </section>

              <section className="content-grid">
                <article className="panel daily-panel">
                  <div className="panel-heading">
                    <div>
                      <h3>Today's learning</h3>
                      <p>A small step makes a big difference.</p>
                    </div>
                    <span className="today-tag">TODAY</span>
                  </div>

                  <div className="daily-task">
                    <div className="task-icon">Aa</div>
                    <div className="task-info">
                      <strong>Academic Vocabulary</strong>
                      <p>Learn essential academic words</p>
                      <span>{savedWords.length} saved words</span>
                    </div>
                    <button
                      className="start-button"
                      onClick={() => setCurrentPage('vocabulary')}
                    >
                      My Vocabulary →
                    </button>
                  </div>

                  <div className="daily-task">
                    <div className="task-icon reading-icon">文</div>
                    <div className="task-info">
                      <strong>Vocabulary Review</strong>
                      <p>Review your saved academic words</p>
                      <span>Practice your vocabulary</span>
                    </div>
                    <button
                      className="start-button"
                      onClick={startReview}
                      disabled={savedWords.length === 0}
                    >
                      Review →
                    </button>
                  </div>
                </article>

                <article className="panel goal-panel">
                  <h3>Your weekly goal</h3>
                  <p>Consistency is more important than perfection.</p>

                  <div className="goal-number">
                    <strong>{weeklyStudyDays}</strong>
                    <span>/ 5 study days</span>
                  </div>

                  <div className="progress-track">
                    <div
                      className="progress-fill"
                      style={{
                        width: `${Math.min(100, (weeklyStudyDays / 5) * 100)}%`,
                      }}
                    />
                  </div>

                  <span className="goal-caption">
                    Keep building your learning habit.
                  </span>
                </article>
              </section>

            </>
          )}

          {/* ================================= */}
          {/* MY VOCABULARY */}
          {/* ================================= */}

          {currentPage === 'vocabulary' && (
            <>
              <section className="welcome">
                <div>
                  <p className="eyebrow">YOUR PERSONAL COLLECTION</p>
                  <h2>My Vocabulary</h2>
                  <p className="welcome-description">
                    Keep track of the academic words you want to remember.
                  </p>
                </div>
                <div className="welcome-decoration">Aa</div>
              </section>

              <section className="panel" style={{ padding: '24px' }}>
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    flexWrap: 'wrap',
                    gap: '12px',
                  }}
                >
                  <div>
                    <h3>Saved Words</h3>
                    <p style={{ color: '#64748B' }}>
                      {savedWords.length} words in your collection
                    </p>
                  </div>

                  <button
                    className="start-button"
                    onClick={startReview}
                    disabled={savedWords.length === 0}
                  >
                    Start Review →
                  </button>
                </div>

                {savedWords.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '50px 16px' }}>
                    <div style={{ fontSize: '40px' }}>📚</div>
                    <h3>Your vocabulary collection is empty.</h3>
                    <p style={{ color: '#64748B' }}>
                      Analyze a text and save words you want to learn.
                    </p>
                    <button
                      className="start-button"
                      onClick={() => setCurrentPage('dashboard')}
                    >
                      Go to Analyzer →
                    </button>
                  </div>
                ) : (
                  savedWords.map((item) => (
                    <div
                      key={item.word}
                      style={{
                        padding: '18px',
                        marginTop: '12px',
                        border: '1px solid #E2E8F0',
                        borderRadius: '10px',
                        background: '#FFFFFF',
                      }}
                    >
                      <div
                        style={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          flexWrap: 'wrap',
                          gap: '12px',
                        }}
                      >
                        <strong style={{ fontSize: '18px' }}>
                          {item.word}
                        </strong>
                        <span style={{ color: '#356AE6' }}>
                          {item.category}
                        </span>
                      </div>

                      <p style={{ margin: '8px 0' }}>
                        {item.japanese || 'Japanese meaning unavailable'}
                      </p>

                      <p style={{ color: '#64748B' }}>
                        {item.definition || 'Definition unavailable'}
                      </p>

                      <small style={{ color: '#64748B' }}>
                        {item.level || 'Level not classified'}
                      </small>

                      <p style={{ color: '#64748B', lineHeight: 1.7 }}>
                        <strong>Original sentence:</strong>{' '}
                        {item.sourceSentence || 'Original sentence unavailable.'}
                      </p>

                      <p style={{ fontSize: '13px', color: '#64748B' }}>
                        {masteredWords.includes(item.word)
                          ? '✓ Mastered'
                          : practiceWords.includes(item.word)
                            ? '↻ Needs practice'
                            : 'Not reviewed yet'}
                      </p>

                      <button
                        onClick={() => removeSavedWord(item.word)}
                        style={{
                          padding: '8px 14px',
                          border: '1px solid #D94B4B',
                          borderRadius: '8px',
                          background: '#FFFFFF',
                          color: '#D94B4B',
                          cursor: 'pointer',
                        }}
                      >
                        Remove Word
                      </button>
                    </div>
                  ))
                )}
              </section>
            </>
          )}

          {/* ================================= */}
          {/* REVIEW MODE */}
          {/* ================================= */}

          {currentPage === 'review' && (
            <>
              <section className="welcome">
                <div>
                  <p className="eyebrow">PRACTICE MAKES PROGRESS</p>
                  <h2>Review Mode</h2>
                  <p className="welcome-description">
                    Test your memory and strengthen your academic vocabulary.
                  </p>
                </div>
                <div className="welcome-decoration">?</div>
              </section>

              <section className="panel" style={{ padding: '24px' }}>
                {reviewFeedback && (
                  <p
                    className="review-feedback"
                    role="status"
                    style={{ color: '#16845B', marginBottom: '16px' }}
                  >
                    {reviewFeedback}
                  </p>
                )}

                {savedWords.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '40px 16px' }}>
                    <h3>No saved words to review yet.</h3>
                    <p style={{ color: '#64748B' }}>
                      Save some vocabulary words first.
                    </p>
                    <button
                      className="start-button"
                      onClick={() => setCurrentPage('dashboard')}
                    >
                      Go to Analyzer →
                    </button>
                  </div>
                ) : (
                  <>
                    <div
                      style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        flexWrap: 'wrap',
                        gap: '12px',
                      }}
                    >
                      <h3>Vocabulary Practice</h3>
                      <span style={{ color: '#64748B' }}>
                        Card {reviewIndex + 1} of {savedWords.length}
                      </span>
                    </div>

                    <div
                      style={{
                        height: '6px',
                        background: '#E2E8F0',
                        borderRadius: '10px',
                        margin: '16px 0 28px',
                        overflow: 'hidden',
                      }}
                    >
                      <div
                        style={{
                          height: '100%',
                          width: `${((reviewIndex + 1) / savedWords.length) * 100}%`,
                          background: '#356AE6',
                          borderRadius: '10px',
                        }}
                      />
                    </div>

                    <div
                      style={{
                        textAlign: 'center',
                        padding: '35px 20px',
                        border: '1px solid #E2E8F0',
                        borderRadius: '14px',
                        background: '#FFFFFF',
                      }}
                    >
                      <p
                        style={{
                          color: '#64748B',
                          fontSize: '13px',
                          letterSpacing: '1px',
                        }}
                      >
                        WHAT DOES THIS WORD MEAN?
                      </p>

                      <h2 style={{ fontSize: '36px', color: '#17345B' }}>
                        {currentReviewWord?.word}
                      </h2>

                      {currentReviewWord?.level && (
                        <p style={{ color: '#64748B' }}>
                          {currentReviewWord.level}
                        </p>
                      )}

                      {!showAnswer ? (
                        <button
                          style={primaryButtonStyle}
                          onClick={() => setShowAnswer(true)}
                        >
                          Reveal Answer
                        </button>
                      ) : (
                        <div
                          style={{
                            marginTop: '20px',
                            padding: '18px',
                            background: '#F4F7FC',
                            borderRadius: '10px',
                            textAlign: 'left',
                          }}
                        >
                          <h3>
                            {currentReviewWord?.japanese || 'Meaning unavailable'}
                          </h3>

                          <p style={{ color: '#64748B', lineHeight: 1.7 }}>
                            {currentReviewWord?.definition || 'Definition unavailable'}
                          </p>

                          <p>
                            <strong>Category:</strong>{' '}
                            {currentReviewWord?.category}
                          </p>

                          <div
                            style={{
                              display: 'flex',
                              justifyContent: 'center',
                              gap: '12px',
                              flexWrap: 'wrap',
                              marginTop: '20px',
                            }}
                          >
                            <button
                              onClick={() =>
                                currentReviewWord &&
                                markWordAsMastered(currentReviewWord.word)
                              }
                              style={{
                                padding: '12px 18px',
                                background: '#E9F7F0',
                                color: '#16845B',
                                border: '1px solid #16845B',
                                borderRadius: '8px',
                                cursor: 'pointer',
                              }}
                            >
                              ✓ I know this word
                            </button>

                            <button
                              onClick={() =>
                                currentReviewWord &&
                                markWordForPractice(currentReviewWord.word)
                              }
                              style={{
                                padding: '12px 18px',
                                background: '#FFF7E8',
                                color: '#D99525',
                                border: '1px solid #D99525',
                                borderRadius: '8px',
                                cursor: 'pointer',
                              }}
                            >
                              ↻ Need more practice
                            </button>
                          </div>
                        </div>
                      )}
                    </div>

                    <div
                      style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        gap: '12px',
                        marginTop: '24px',
                      }}
                    >
                      <button
                        style={filterButtonStyle(false)}
                        disabled={reviewIndex === 0}
                        onClick={goToPreviousWord}
                      >
                        ← Previous
                      </button>

                      <button
                        style={primaryButtonStyle}
                        onClick={goToNextWord}
                      >
                        {reviewIndex === savedWords.length - 1
                          ? 'Start Again ↻'
                          : 'Next Word →'}
                      </button>
                    </div>
                  </>
                )}
              </section>
            </>
          )}

          {/* ================================= */}
          {/* LEARNING PROGRESS */}
          {/* ================================= */}

          {currentPage === 'progress' && (
            <>
              <section className="welcome">
                <div>
                  <p className="eyebrow">YOUR LEARNING JOURNEY</p>
                  <h2>Learning Analytics</h2>
                  <p className="welcome-description">
                    Understand your progress and keep improving.
                  </p>
                </div>
                <div className="welcome-decoration">↗</div>
              </section>

              <section className="stats-grid">
                <article className="stat-card">
                  <span className="stat-icon">📚</span>
                  <p>Words Saved</p>
                  <strong>{savedWords.length}</strong>
                  <span className="stat-note">Total vocabulary collected</span>
                </article>

                <article className="stat-card">
                  <span className="stat-icon">🎓</span>
                  <p>Mastered Words</p>
                  <strong>{validMasteredCount}</strong>
                  <span className="stat-note">Words marked as mastered</span>
                </article>

                <article className="stat-card">
                  <span className="stat-icon">↻</span>
                  <p>Need Practice</p>
                  <strong>{practiceWords.length}</strong>
                  <span className="stat-note">Words to review again</span>
                </article>
              </section>

              <section className="panel" style={{ padding: '24px', marginTop: '24px' }}>
                <h3>Vocabulary Mastery</h3>
                <p style={{ color: '#64748B' }}>
                  Your self-reported vocabulary mastery rate
                </p>

                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    marginTop: '24px',
                  }}
                >
                  <strong>Overall Progress</strong>
                  <strong style={{ color: '#356AE6' }}>{masteryRate}%</strong>
                </div>

                <div
                  style={{
                    height: '14px',
                    background: '#E2E8F0',
                    borderRadius: '20px',
                    overflow: 'hidden',
                    marginTop: '12px',
                  }}
                >
                  <div
                    style={{
                      height: '100%',
                      width: `${masteryRate}%`,
                      background: '#356AE6',
                      borderRadius: '20px',
                      transition: 'width 0.3s ease',
                    }}
                  />
                </div>

                <p style={{ color: '#64748B', marginTop: '12px' }}>
                  {validMasteredCount} mastered out of {savedWords.length} saved words.
                </p>
              </section>

              <section className="panel" style={{ padding: '24px', marginTop: '24px' }}>
                <h3>Vocabulary Status</h3>

                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
                    gap: '14px',
                    marginTop: '18px',
                  }}
                >
                  <div style={{ padding: '18px', borderRadius: '10px', background: '#E9F7F0' }}>
                    <p style={{ color: '#16845B', margin: 0 }}>Mastered</p>
                    <strong style={{ fontSize: '26px', color: '#16845B' }}>
                      {validMasteredCount}
                    </strong>
                  </div>

                  <div style={{ padding: '18px', borderRadius: '10px', background: '#FFF7E8' }}>
                    <p style={{ color: '#D99525', margin: 0 }}>Need Practice</p>
                    <strong style={{ fontSize: '26px', color: '#D99525' }}>
                      {practiceWords.filter((word) =>
                        savedWords.some((item) => item.word === word)
                      ).length}
                    </strong>
                  </div>

                  <div style={{ padding: '18px', borderRadius: '10px', background: '#F4F7FC' }}>
                    <p style={{ color: '#64748B', margin: 0 }}>Not Reviewed</p>
                    <strong style={{ fontSize: '26px' }}>
                      {savedWords.filter(
                        (item) =>
                          !masteredWords.includes(item.word) &&
                          !practiceWords.includes(item.word)
                      ).length}
                    </strong>
                  </div>
                </div>
              </section>

              <section className="panel" style={{ padding: '24px', marginTop: '24px' }}>
                <h3>Study History</h3>
                <p style={{ color: '#64748B' }}>
                  Days when you analyzed text or reviewed vocabulary.
                </p>

                <div
                  style={{
                    marginTop: '20px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    flexWrap: 'wrap',
                    gap: '12px',
                  }}
                >
                  <div>
                    <strong style={{ fontSize: '30px' }}>
                      {studyHistory.length}
                    </strong>
                    <p style={{ color: '#64748B', margin: 0 }}>
                      Total study days
                    </p>
                  </div>

                  <div>
                    <strong style={{ fontSize: '24px' }}>
                      {studyHistory.length === 0
                        ? '—'
                        : new Date(
                            `${[...studyHistory].sort().at(-1)}T12:00:00`
                          ).toLocaleDateString()}
                    </strong>
                    <p style={{ color: '#64748B', margin: 0 }}>
                      Most recent study day
                    </p>
                  </div>
                </div>

                {studyHistory.length === 0 ? (
                  <p style={{ color: '#64748B', marginTop: '24px' }}>
                    Your study history will appear here after your first learning session.
                  </p>
                ) : (
                  <div
                    style={{
                      display: 'flex',
                      flexWrap: 'wrap',
                      gap: '8px',
                      marginTop: '20px',
                    }}
                  >
                    {[...studyHistory].sort().reverse().map((date) => (
                      <span
                        key={date}
                        style={{
                          padding: '8px 12px',
                          borderRadius: '8px',
                          background: '#EAF1FF',
                          color: '#356AE6',
                          fontSize: '13px',
                        }}
                      >
                        {date}
                      </span>
                    ))}
                  </div>
                )}
              </section>

              <section className="panel" style={{ padding: '24px', marginTop: '24px' }}>
                <h3>Recommended Next Step</h3>

                {practiceWords.length > 0 ? (
                  <>
                    <p style={{ color: '#64748B' }}>
                      You have {practiceWords.length} word(s) marked for additional practice.
                    </p>
                    <button className="start-button" onClick={startReview}>
                      Continue Reviewing →
                    </button>
                  </>
                ) : savedWords.length > 0 ? (
                  <>
                    <p style={{ color: '#64748B' }}>
                      Keep reviewing your saved vocabulary to strengthen your memory.
                    </p>
                    <button className="start-button" onClick={startReview}>
                      Start Vocabulary Review →
                    </button>
                  </>
                ) : (
                  <>
                    <p style={{ color: '#64748B' }}>
                      Start by analyzing an academic English paragraph and saving useful vocabulary.
                    </p>
                    <button
                      className="start-button"
                      onClick={() => setCurrentPage('dashboard')}
                    >
                      Go to Vocabulary Analyzer →
                    </button>
                  </>
                )}
              </section>
            </>
          )}

          {/* ================================= */}
          {/* WRITING ANALYZER */}
          {/* ================================= */}

          {currentPage === 'writing' && (
            <>
              <section className="welcome">
                <div>
                  <p className="eyebrow">ACADEMIC WRITING DEVELOPMENT</p>
                  <h2>Writing Analyzer</h2>
                  <p className="welcome-description">
                    Improve your academic writing, one sentence at a time.
                  </p>
                </div>
                <div className="welcome-decoration">W</div>
              </section>

              <section className="panel" style={{ padding: '24px' }}>
                <h3>Analyze Your Writing</h3>
                <p style={{ color: '#64748B' }}>
                  Paste your essay or academic paragraph below.
                </p>

                <textarea
                  value={writingText}
                  onChange={(event) => setWritingText(event.target.value)}
                  placeholder="Paste your academic writing here..."
                  rows={10}
                  style={{
                    width: '100%',
                    padding: '14px',
                    marginTop: '12px',
                    border: '1px solid #E2E8F0',
                    borderRadius: '10px',
                    fontSize: '15px',
                    resize: 'vertical',
                    boxSizing: 'border-box',
                  }}
                />

                <button
                  className="start-button"
                  style={{ marginTop: '14px' }}
                  onClick={handleWritingAnalysis}
                  disabled={!writingText.trim() || writingLoading}
                >
                  {writingLoading ? 'Analyzing...' : 'Analyze My Writing →'}
                </button>

                {writingError && (
                  <p style={{ color: '#D94B4B', marginTop: '12px' }}>
                    {writingError}
                  </p>
                )}

                {writingResult && (
                  <div style={{ marginTop: '28px' }}>
                    <h3>Analysis Results</h3>
                    <p style={{ color: '#64748B' }}>
                      Initial vocabulary analysis of your writing.
                    </p>

                    <div
                      style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                        gap: '14px',
                        marginTop: '20px',
                      }}
                    >
                      <div style={summaryCardStyle}>
                        <p style={{ color: '#64748B', margin: 0 }}>Total Words</p>
                        <strong style={{ fontSize: '28px' }}>
                          {writingResult.total_words}
                        </strong>
                      </div>

                      <div style={summaryCardStyle}>
                        <p style={{ color: '#64748B', margin: 0 }}>Needs Review</p>
                        <strong style={{ fontSize: '28px', color: '#D99525' }}>
                          {writingResult.review_count}
                        </strong>
                      </div>
                    </div>

                    <h3 style={{ marginTop: '24px' }}>
                      Vocabulary Findings
                    </h3>

                    {writingResult.results.length === 0 ? (
                      <p style={{ color: '#64748B' }}>
                        No vocabulary results were returned.
                      </p>
                    ) : (
                      writingResult.results.map((item, index) => (
                        <div
                          key={`${item.word}-${index}`}
                          style={{
                            padding: '14px',
                            marginTop: '10px',
                            border: '1px solid #E2E8F0',
                            borderRadius: '10px',
                            background: '#FFFFFF',
                          }}
                        >
                          <strong>{item.word}</strong>
                          <p style={{ color: '#356AE6' }}>
                            {item.category}
                          </p>
                          {item.japanese && <p>{item.japanese}</p>}
                          {item.definition && (
                            <p style={{ color: '#64748B' }}>
                              {item.definition}
                            </p>
                          )}
                        </div>
                      ))
                    )}
                  </div>
                )}
              </section>

              <section className="panel" style={{ padding: '24px', marginTop: '24px' }}>
                <h3>Future Writing Tools</h3>
                <p style={{ color: '#64748B' }}>
                  These features are planned for future development. They are not active yet.
                </p>

                <div className="stats-grid" style={{ marginTop: '18px' }}>
                  {[
                    ['Grammar Analysis', 'Sentence accuracy'],
                    ['Academic Tone', 'Formal language'],
                    ['Sentence Structure', 'Sentence variety'],
                    ['Cohesion', 'Logical connections'],
                  ].map(([title, description]) => (
                    <article className="stat-card" key={title}>
                      <span className="stat-icon">✦</span>
                      <p>{title}</p>
                      <span className="stat-note">
                        {description} · Coming soon
                      </span>
                    </article>
                  ))}
                </div>
              </section>
            </>
          )}

          {/* ================================= */}
          {/* LISTENING */}
          {/* ================================= */}

          {currentPage === 'listening' && (
            <ListeningPage />
          )}

         

          
{/* ================================= */}
{/* SPEAKING */}
{/* ================================= */}

{currentPage === 'speaking' && (
  <SpeakingPage />
)}

                


          {/* ================================= */}
          {/* SETTINGS */}
          {/* ================================= */}

          {currentPage === 'settings' && (
            <>
              <section className="welcome">
                <div>
                  <p className="eyebrow">PERSONALIZE YOUR EXPERIENCE</p>
                  <h2>Settings</h2>
                  <p className="welcome-description">
                    Manage your ACADEMIA preferences.
                  </p>
                </div>
                <div className="welcome-decoration">⚙</div>
              </section>

              <section className="panel" style={{ padding: '24px' }}>
                <h3>Interface Language</h3>
                <p style={{ color: '#64748B' }}>
                  Choose your preferred interface language.
                </p>

                <div
                  style={{
                    display: 'flex',
                    gap: '12px',
                    flexWrap: 'wrap',
                    marginTop: '18px',
                  }}
                >
                  <button
                    style={filterButtonStyle(interfaceLanguage === 'EN')}
                    onClick={() => setInterfaceLanguage('EN')}
                  >
                    English
                  </button>

                  <button
                    style={filterButtonStyle(interfaceLanguage === 'JP')}
                    onClick={() => setInterfaceLanguage('JP')}
                  >
                    日本語
                  </button>
                </div>

                <p style={{ color: '#64748B', marginTop: '14px' }}>
                  Current preference: {interfaceLanguage === 'EN' ? 'English' : 'Japanese'}
                </p>

                <p style={{ color: '#D99525', marginTop: '8px' }}>
                  Note: This setting currently saves your preference. Full interface translation is not implemented yet.
                </p>
              </section>

              <section className="panel" style={{ padding: '24px', marginTop: '24px' }}>
                <h3>Your Learning Data</h3>
                <p style={{ color: '#64748B' }}>
                  Your vocabulary and study history are stored in this browser.
                </p>

                <div style={{ marginTop: '18px' }}>
                  <p>Saved words: <strong>{savedWords.length}</strong></p>
                  <p>Mastered words: <strong>{validMasteredCount}</strong></p>
                  <p>Practice words: <strong>{practiceWords.length}</strong></p>
                  <p>Study days: <strong>{studyHistory.length}</strong></p>
                </div>
              </section>
            </>
          )}

          {/* ================================= */}
          {/* FOOTER */}
          {/* ================================= */}

          <footer className="dashboard-footer">
            <span>ACADEMIA</span>
            <span>Learn beyond everyday English.</span>
          </footer>

        </div>
      </main>
    </div>
  )
}

export default App
