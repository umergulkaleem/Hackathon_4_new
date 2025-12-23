import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Learn ROS 2 Fundamentals',
    description: (
      <>
        Understand the core concepts of ROS 2 middleware, including the ROS graph,
        DDS (Data Distribution Service), and how to connect AI agents to humanoid robots.
      </>
    ),
  },
  {
    title: 'Master Communication Patterns',
    description: (
      <>
        Implement nodes, topics, services, and actions using Python and rclpy
        to control robots with AI agents.
      </>
    ),
  },
  {
    title: 'Model Humanoid Robots',
    description: (
      <>
        Create and understand URDF models for humanoid robots, defining links,
        joints, and frames for robot control.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}