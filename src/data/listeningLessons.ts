
export type ListeningQuestion = {
  id: number
  type:
    | 'Main Idea'
    | 'Supporting Details'
    | 'Inference'
    | 'Speaker Purpose'
  question: string
  options: string[]
  correctAnswer: string
  explanation: string
}

export type ListeningCategory =
  | 'Lifestyle & Vlogs'
  | 'Education & Academic'
  | 'Entertainment & Fun'
  | 'Documentary & Society'
  | 'Podcasts & Conversations'
  | 'Science & Technology'
  | 'Travel & Culture'
  | 'News & Current Affairs'

export type SubtitleSegment = {
  id: number
  startTime: number
  endTime: number
  text: string
}

export type ListeningLesson = {
  id: number
  title: string
  source: string
  sourceType: 'YouTube' | 'Podcast' | 'Radio' | 'Official Website'

  // Content classification
  category: ListeningCategory
  subcategory?: string

  // Learning information
  level: 'Beginner' | 'Intermediate' | 'Advanced'
  learningFocus: string[]
  duration: string
  description: string

  // Media information
  mediaType: 'video' | 'audio'
  url: string
  embedUrl?: string

  // Learning materials
  transcript?: string
  subtitles?: SubtitleSegment[]
  questions?: ListeningQuestion[]
  skillFocus?: string[]
}

export const listeningLessons: ListeningLesson[] = [
  {
    id: 1,
    title: 'Introduction to Academic Listening',
    source: 'TED',
    sourceType: 'Official Website',
    category: 'Education & Academic',
    subcategory: 'Academic Skills',
    level: 'Beginner',
    learningFocus: ['Listening', 'Academic Vocabulary'],
    duration: '5–10 min',
    description: 'Learn how to identify the main idea of a presentation.',
    mediaType: 'video',
    url: 'https://www.ted.com/talks',
    transcript: `
Welcome to academic listening.
Today, we will explore how to understand the main idea of a presentation.
Good listeners do not simply hear words.
They identify key information, supporting details, and the speaker's purpose.
Let's begin by discussing the main idea.
    `,
    subtitles: [
      {
        id: 1,
        startTime: 0,
        endTime: 4,
        text: 'Welcome to academic listening.'
      },
      {
        id: 2,
        startTime: 4,
        endTime: 9,
        text: 'Today, we will explore how to understand the main idea of a presentation.'
      },
      {
        id: 3,
        startTime: 9,
        endTime: 14,
        text: 'Good listeners do not simply hear words.'
      },
      {
        id: 4,
        startTime: 14,
        endTime: 21,
        text: 'They identify key information, supporting details, and the speaker’s purpose.'
      }
    ],
    skillFocus: ['Main Idea', 'Supporting Details']
  },

  {
    id: 2,
    title: 'Understanding Human Behaviour',
    source: 'BBC',
    sourceType: 'Radio',
    category: 'Documentary & Society',
    subcategory: 'Psychology',
    level: 'Intermediate',
    learningFocus: ['Listening', 'Critical Thinking'],
    duration: '10–15 min',
    description: 'Explore human behaviour and identify supporting details.',
    mediaType: 'audio',
    url: 'https://www.bbc.com/audio'
  },

  {
    id: 3,
    title: 'The Future of Education',
    source: 'NPR',
    sourceType: 'Podcast',
    category: 'Education & Academic',
    subcategory: 'Education',
    level: 'Advanced',
    learningFocus: ['Academic Vocabulary', 'Critical Thinking'],
    duration: '15–20 min',
    description: 'Analyze arguments, perspectives, and evidence.',
    mediaType: 'audio',
    url: 'https://www.npr.org/podcasts/'
  }
]
