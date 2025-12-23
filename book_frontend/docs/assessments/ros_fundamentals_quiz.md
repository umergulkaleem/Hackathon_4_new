---
sidebar_label: 'ROS 2 Fundamentals Quiz'
sidebar_position: 4
---

# ROS 2 Fundamentals Assessment

Test your understanding of ROS 2 fundamentals with this interactive quiz.

import Assessment from '@site/src/components/Assessment';

## Question 1

<Assessment
  question="What does DDS stand for in the context of ROS 2?"
  options={[
    "Data Distribution Service",
    "Dynamic Discovery System",
    "Distributed Data Storage",
    "Direct Data Sharing"
  ]}
  correctAnswer="Data Distribution Service"
  explanation="DDS (Data Distribution Service) is a middleware specification that enables scalable, real-time, dependable, and efficient data exchanges between devices. In ROS 2, DDS provides the underlying communication infrastructure."
/>

## Question 2

<Assessment
  question="Which of the following is NOT a communication pattern in ROS 2?"
  options={[
    "Topics",
    "Services",
    "Actions",
    "Databases"
  ]}
  correctAnswer="Databases"
  explanation="ROS 2 provides three main communication patterns: Topics (publish/subscribe), Services (request/response), and Actions (goal-oriented with feedback). Databases are not a native communication pattern in ROS 2."
/>

## Question 3

<Assessment
  question="What is the primary purpose of a ROS 2 node?"
  options={[
    "To store data permanently",
    "To serve as a process that performs computation and communicates with other nodes",
    "To manage hardware drivers only",
    "To provide user interfaces"
  ]}
  correctAnswer="To serve as a process that performs computation and communicates with other nodes"
  explanation="A node is a process that performs computation. Nodes are combined together into a ROS graph to do work. They can publish or subscribe to topics, provide or use services, and send or execute actions."
/>