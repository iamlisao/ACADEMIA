
import { useState } from 'react'

const speakingTopics = [
  {
    id: 1,
    title: 'Technology in Education',
    category: 'Education',
    level: 'Beginner',
    question: 'Should technology be used in education?',
    time: '1 minute',
  },
  {
    id: 2,
    title: 'Climate Change',
    category: 'Environment',
    level: 'Intermediate',
    question: 'What are the most effective ways to address climate change?',
    time: '2 minutes',
  },
  {
    id: 3,
    title: 'Social Media and Society',
    category: 'Society',
    level: 'Intermediate',
    question: 'How does social media influence the way people think?',
    time: '2 minutes',
  },
  {
    id: 4,
    title: 'Artificial Intelligence',
    category: 'Technology',
    level: 'Advanced',
    question: 'To what extent should society rely on artificial intelligence?',
    time: '3 minutes',
  },
]

function SpeakingPage() {
  const [selectedTopic, setSelectedTopic] = useState(
    speakingTopics[0]
  )
  const [answer, setAnswer] = useState('')
  const [showTips, setShowTips] = useState(false)

  return (
    <div className="speaking-page">
      <header className="speaking-header">
        <p className="speaking-eyebrow">ACADEMIA LEARNING</p>
        <h1>Academic Speaking</h1>
        <p>
          Develop confidence and express your ideas in academic English.
        </p>
      </header>

      <section className="speaking-intro">
        <h2>Find Your Academic Voice.</h2>
        <p>
          Practice expressing opinions, supporting arguments,
          and communicating complex ideas.
        </p>
      </section>

      <section className="speaking-topics">
        <div className="speaking-section-heading">
          <h2>Choose a Speaking Topic</h2>
          <span>{speakingTopics.length} topics</span>
        </div>

        <div className="speaking-topic-grid">
          {speakingTopics.map((topic) => (
            <button
              key={topic.id}
              className={`speaking-topic-card ${
                selectedTopic.id === topic.id ? 'selected' : ''
              }`}
              onClick={() => {
                setSelectedTopic(topic)
                setAnswer('')
              }}
            >
              <span>{topic.category}</span>
              <h3>{topic.title}</h3>
              <p>{topic.level} · {topic.time}</p>
            </button>
          ))}
        </div>
      </section>

      <section className="speaking-practice">
        <p className="speaking-eyebrow">YOUR SPEAKING CHALLENGE</p>
        <h2>{selectedTopic.title}</h2>
        <p className="speaking-question">
          {selectedTopic.question}
        </p>

        <label htmlFor="speaking-answer">
          Plan your answer (optional)
        </label>
        <textarea
          id="speaking-answer"
          value={answer}
          onChange={(event) => setAnswer(event.target.value)}
          placeholder="Write down your main ideas before speaking..."
          rows={5}
        />

        <button
          className="speaking-tips-button"
          onClick={() => setShowTips(!showTips)}
        >
          {showTips ? 'Hide' : 'Show'} Speaking Tips
        </button>

        {showTips && (
          <div className="speaking-tips">
            <h3>How to structure your answer</h3>
            <ol>
              <li>State your opinion clearly.</li>
              <li>Give a reason to support your opinion.</li>
              <li>Provide a specific example or evidence.</li>
              <li>Finish with a clear conclusion.</li>
            </ol>
            <p>
              Useful phrases: "In my opinion...", 
              "One significant reason is...", 
              "For example...", 
              "Therefore..."
            </p>
          </div>
        )}
      </section>

      <section className="speaking-feedback">
        <h2>Speaking Feedback</h2>
        <p>
          Recording and AI-powered speaking evaluation
          will be added in a future update.
        </p>
        <div className="speaking-feedback-grid">
          <span>Pronunciation</span>
          <span>Fluency</span>
          <span>Grammar</span>
          <span>Vocabulary</span>
          <span>Organization</span>
          <span>Critical Thinking</span>
        </div>
      </section>
    </div>
  )
}

export default SpeakingPage
