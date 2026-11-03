
import type { ListeningLesson } from '../data/listeningLessons'

type Props = {
  lesson: ListeningLesson
  onSelect: (lesson: ListeningLesson) => void
}

function ListeningCard({ lesson, onSelect }: Props) {
  return (
    <article className="listening-card">
      <div className="listening-card-top">
        <span className="listening-source">{lesson.source}</span>
        <span className={`listening-level ${lesson.level.toLowerCase()}`}>
          {lesson.level}
        </span>
      </div>

      <h3>{lesson.title}</h3>

      <p>{lesson.description}</p>

      <div className="listening-card-info">
        <span>{lesson.category}</span>
        <span>{lesson.duration}</span>
      </div>

      <button
        className="listening-start-button"
        onClick={() => onSelect(lesson)}
      >
        Start Listening →
      </button>
    </article>
  )
}

export default ListeningCard
