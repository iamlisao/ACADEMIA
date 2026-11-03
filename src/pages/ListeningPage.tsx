
import { useState } from 'react'
import {
  listeningLessons,
  type ListeningLesson
} from '../data/listeningLessons'
import ListeningCard from '../components/ListeningCard'

function ListeningPage() {
  const [selectedLevel, setSelectedLevel] = useState('All')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [activeLesson, setActiveLesson] = useState<ListeningLesson | null>(null)
  const [showTranscript, setShowTranscript] = useState(false)

  const filteredLessons = listeningLessons.filter((lesson) => {
    const matchesLevel =
      selectedLevel === 'All' || lesson.level === selectedLevel

    const matchesCategory =
      selectedCategory === 'All' || lesson.category === selectedCategory

    return matchesLevel && matchesCategory
  })

  const handleSelectLesson = (lesson: ListeningLesson) => {
    setActiveLesson(lesson)
    setShowTranscript(false)
  }

  const handleBack = () => {
    setActiveLesson(null)
    setShowTranscript(false)
  }

  if (activeLesson) {
    return (
      <div className="listening-page">
        <button className="listening-start-button" onClick={handleBack}>
          ← Back to Library
        </button>

        <header className="listening-header">
          <p className="listening-eyebrow">
            {activeLesson.source} · {activeLesson.level}
          </p>
          <h1>{activeLesson.title}</h1>
          <p>{activeLesson.description}</p>
        </header>

        <section className="listening-card">
          <h2>Listening Material</h2>
          <p>
            Open the official source to listen to this lesson.
          </p>
          <a
            href={activeLesson.url}
            target="_blank"
            rel="noopener noreferrer"
          >
            Open Official Audio →
          </a>
        </section>

        <section className="listening-card">
          <div className="listening-section-heading">
            <h2>Transcript</h2>
            <button
              className="listening-start-button"
              onClick={() => setShowTranscript(!showTranscript)}
            >
              {showTranscript ? 'Hide Transcript' : 'Show Transcript'}
            </button>
          </div>

          {showTranscript && (
            <div>
              {activeLesson.transcript ? (
                <p>{activeLesson.transcript}</p>
              ) : (
                <p>
                  Transcript is not available for this lesson yet.
                </p>
              )}
            </div>
          )}
        </section>

        <section className="listening-card">
          <h2>Comprehension Check</h2>

          {activeLesson.questions?.length ? (
            activeLesson.questions.map((question) => (
              <div key={question.id}>
                <p>{question.type}</p>
                <h3>{question.question}</h3>
                {question.options.map((option) => (
                  <p key={option}>• {option}</p>
                ))}
              </div>
            ))
          ) : (
            <p>
              Comprehension questions will be available soon.
            </p>
          )}
        </section>
      </div>
    )
  }

  return (
    <div className="listening-page">
      <header className="listening-header">
        <p className="listening-eyebrow">ACADEMIA LEARNING</p>
        <h1>Listening Library</h1>
        <p>
          Explore authentic English content from around the world.
        </p>
      </header>

      <section className="listening-filters">
        <div>
          <label htmlFor="level-filter">Difficulty</label>
          <select
            id="level-filter"
            value={selectedLevel}
            onChange={(event) => setSelectedLevel(event.target.value)}
          >
            <option value="All">All Levels</option>
            <option value="Beginner">Beginner</option>
            <option value="Intermediate">Intermediate</option>
            <option value="Advanced">Advanced</option>
          </select>
        </div>

        <div>
          <label htmlFor="category-filter">Category</label>
          <select
            id="category-filter"
            value={selectedCategory}
            onChange={(event) => setSelectedCategory(event.target.value)}
          >
            <option value="All">All Categories</option>
            <option value="Education">Education</option>
            <option value="Psychology">Psychology</option>
            <option value="Environment">Environment</option>
            <option value="Society">Society</option>
          </select>
        </div>
      </section>

      <section className="listening-lessons">
        <div className="listening-section-heading">
          <h2>Featured Lessons</h2>
          <span>{filteredLessons.length} lessons</span>
        </div>

        {filteredLessons.length > 0 ? (
          <div className="listening-grid">
            {filteredLessons.map((lesson) => (
              <ListeningCard
                key={lesson.id}
                lesson={lesson}
                onSelect={handleSelectLesson}
              />
            ))}
          </div>
        ) : (
          <p>No lessons found in this category.</p>
        )}
      </section>
    </div>
  )
}

export default ListeningPage
