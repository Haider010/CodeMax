import React, { useState } from 'react';
import './styles/Study.css';

const Study = () => {
  // State to store the clicked topic index
  const [activeTopic, setActiveTopic] = useState(null);

  // List of topics
  const topics = [
    { name: "Arrays", description: "Learn about arrays, their operations, and applications in DSA." },
    { name: "Linked Lists", description: "Master linked lists and their types: singly, doubly, and circular." },
    { name: "Stacks", description: "Understand the concept of stacks and their usage in DSA." },
    { name: "Queues", description: "Learn about queues, dequeue, and circular queues." },
    { name: "Hashing", description: "Explore hashing techniques and hash tables." },
    { name: "Trees", description: "Dive into trees, binary trees, and binary search trees." },
    { name: "Heaps", description: "Learn about heaps, priority queues, and heap operations." },
    { name: "Graphs", description: "Understand graphs, graph traversal algorithms, and applications." },
    { name: "Sorting", description: "Master sorting algorithms: Bubble Sort, Merge Sort, Quick Sort, etc." },
    { name: "Searching", description: "Learn about searching algorithms: Linear Search, Binary Search, etc." },
    { name: "Dynamic Programming", description: "Learn techniques for solving optimization problems." },
    { name: "Greedy Algorithms", description: "Understand the greedy approach to solving problems." }
  ];

  // Function to handle the click on a topic
  const handleTopicClick = (index) => {
    setActiveTopic(index === activeTopic ? null : index); // Toggle the active topic description
  };

  return (
    <div className="study-container">
      <h2>Top 12 Topics in DSA</h2>

      {/* Grid layout for topic cards */}
      <div className="topics-list">
        {topics.map((topic, index) => (
          <div
            key={index}
            className="topic-item"
            onClick={() => handleTopicClick(index)} // Handle click to toggle description
          >
            <h3>{topic.name}</h3>
          </div>
        ))}
      </div>

      {/* Display the description of the active topic */}
      {activeTopic !== null && (
        <div className="description-container">
          <h3>{topics[activeTopic].name}</h3>
          <p>{topics[activeTopic].description}</p>
        </div>
      )}
    </div>
  );
};

export default Study;
