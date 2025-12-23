# Data Model: VLA Learning Module

**Feature**: VLA Learning Module
**Created**: 2025-12-17
**Status**: Complete

## Entity: LearningModule

**Description**: Represents a complete learning module containing multiple chapters on VLA concepts.

**Fields**:
- `moduleId`: string (unique identifier for the module)
- `title`: string (display title of the module)
- `description`: string (brief description of the module content)
- `chapters`: Chapter[] (array of chapters in this module)
- `prerequisites`: string[] (list of prerequisite knowledge areas)
- `learningObjectives`: string[] (what students will learn from this module)
- `duration`: number (estimated completion time in minutes)
- `difficulty`: "beginner" | "intermediate" | "advanced" (difficulty level)
- `createdDate`: string (ISO date when module was created)
- `lastUpdated`: string (ISO date when module was last updated)

**Validation Rules**:
- `moduleId` must be unique across all modules
- `title` must be 3-100 characters
- `difficulty` must be one of the specified values
- `duration` must be a positive number

## Entity: Chapter

**Description**: Represents a single chapter within a learning module.

**Fields**:
- `chapterId`: string (unique identifier for the chapter)
- `title`: string (display title of the chapter)
- `content`: string (Markdown content of the chapter)
- `objectives`: string[] (specific learning objectives for this chapter)
- `examples`: Example[] (array of interactive examples in this chapter)
- `exercises`: Exercise[] (array of practice exercises)
- `moduleRef`: string (reference to the parent module)
- `order`: number (sequence order within the module)
- `estimatedTime`: number (time to complete in minutes)

**Validation Rules**:
- `chapterId` must be unique within the module
- `order` must be a positive integer
- `moduleRef` must reference an existing module

## Entity: Example

**Description**: Represents an interactive example demonstrating VLA concepts.

**Fields**:
- `exampleId`: string (unique identifier for the example)
- `title`: string (display title of the example)
- `description`: string (what the example demonstrates)
- `code`: string (code for the example in multiple languages)
- `simulation`: string (simulation environment or scenario)
- `expectedOutput`: string (what students should observe)
- `chapterRef`: string (reference to the parent chapter)
- `type`: "voice" | "vision" | "llm" | "integration" (type of VLA concept)
- `difficulty`: "beginner" | "intermediate" | "advanced"

**Validation Rules**:
- `exampleId` must be unique within the chapter
- `type` must be one of the specified values
- `chapterRef` must reference an existing chapter

## Entity: Exercise

**Description**: Represents a practice exercise for students to test their understanding.

**Fields**:
- `exerciseId`: string (unique identifier for the exercise)
- `title`: string (display title of the exercise)
- `description`: string (what the exercise requires students to do)
- `instructions`: string (step-by-step instructions)
- `solution`: string (reference implementation or expected outcome)
- `chapterRef`: string (reference to the parent chapter)
- `difficulty`: "beginner" | "intermediate" | "advanced"
- `autoGraded`: boolean (whether the exercise can be auto-graded)

**Validation Rules**:
- `exerciseId` must be unique within the chapter
- `chapterRef` must reference an existing chapter

## Entity: SimulationEnvironment

**Description**: Represents a robot simulation environment used for practical examples.

**Fields**:
- `envId`: string (unique identifier for the environment)
- `name`: string (display name of the environment)
- `description`: string (what the environment simulates)
- `robotType`: string (type of robot being simulated)
- `capabilities`: string[] (list of robot capabilities)
- `dockerImage`: string (Docker image for the simulation)
- `configFile`: string (path to configuration file)
- `examples`: string[] (IDs of examples that use this environment)

**Validation Rules**:
- `envId` must be unique
- `dockerImage` must be a valid Docker image reference

## Entity: Assessment

**Description**: Represents a quiz or assessment tool for student evaluation.

**Fields**:
- `assessmentId`: string (unique identifier for the assessment)
- `title`: string (display title of the assessment)
- `type`: "prerequisite" | "chapter" | "module" (type of assessment)
- `questions`: Question[] (array of questions)
- `passingScore`: number (minimum score required to pass)
- `timeLimit`: number (time limit in minutes, 0 for unlimited)
- `targetRef`: string (reference to module or chapter being assessed)

**Validation Rules**:
- `passingScore` must be between 0 and 100
- `timeLimit` must be non-negative

## Entity: Question

**Description**: Represents a single question within an assessment.

**Fields**:
- `questionId`: string (unique identifier for the question)
- `text`: string (the question text)
- `type`: "multiple-choice" | "true-false" | "short-answer" | "code" (question type)
- `options`: string[] (for multiple choice questions)
- `correctAnswer`: string (correct answer)
- `explanation`: string (explanation of the correct answer)
- `assessmentRef`: string (reference to parent assessment)

**Validation Rules**:
- `assessmentRef` must reference an existing assessment
- For multiple-choice, `options` must have 2-6 items

## Relationships

```
LearningModule (1) -- (n) Chapter
Chapter (1) -- (n) Example
Chapter (1) -- (n) Exercise
Example (1) -- (1) SimulationEnvironment (via simulation field)
Assessment (1) -- (n) Question
Chapter (1) -- (n) Assessment (for chapter assessments)
LearningModule (1) -- (n) Assessment (for module assessments)
```

## State Transitions

**Chapter Completion States**:
- `not-started` → `in-progress` → `completed` → `reviewed`

**Module Progress States**:
- `locked` → `available` → `in-progress` → `completed` → `certified`

## Data Validation

All entities must conform to the following validation rules:
- String fields must not exceed 5000 characters unless otherwise specified
- Array fields must have 0-100 elements unless otherwise specified
- All identifiers must follow the format: `[a-z0-9-]+`
- Date fields must be in ISO 8601 format
- References must point to existing entities