// src/components/Study.js
import React, { useState } from 'react';

const topics = [
  { id: 1, name: 'Arrays', description: 'Arrays are used to store multiple values in a single variable.' },
  { id: 2, name: 'Linked List', description: 'A linked list is a linear data structure consisting of a sequence of elements called nodes.' },
  { id: 3, name: 'Stacks', description: 'Stacks are linear data structures that follow the Last In First Out (LIFO) principle.' },
  { id: 4, name: 'Queues', description: 'Queues are linear data structures that follow the First In First Out (FIFO) principle.' },
  { id: 5, name: 'Hashing', description: 'Hashing is a technique used to uniquely identify a specific object from a collection of similar objects.' },
  { id: 6, name: 'Trees', description: 'A tree is a non-linear data structure consisting of a collection of nodes such that each node has a value and references to its children.' },
  { id: 7, name: 'Binary Search Trees', description: 'A binary search tree (BST) is a binary tree with the property that the left child’s value is less than the parent node, and the right child’s value is greater.' },
  { id: 8, name: 'Graphs', description: 'A graph is a collection of nodes (vertices) and edges that connect pairs of nodes.' },
  { id: 9, name: 'Dynamic Programming', description: 'Dynamic programming is a method for solving problems by breaking them down into simpler subproblems and solving each subproblem only once.' },
  { id: 10, name: 'Greedy Algorithms', description: 'Greedy algorithms are a class of algorithms that make the locally optimal choice at each stage in the hope of finding the global optimum.' },
];

const Study = () => {
  const [selectedTopic, setSelectedTopic] = useState(null);

  const handleTopicClick = (topic) => {
    if (selectedTopic === topic.id) {
      setSelectedTopic(null); // Close the topic if it’s already open
    } else {
      setSelectedTopic(topic.id); // Show details for the selected topic
    }
  };

  return (
    <div>
      <h2>Code Academy - DSA Topics</h2>
      <div className="topics-list">
        {topics.map((topic) => (
          <div key={topic.id} className="topic-item" onClick={() => handleTopicClick(topic)}>
            <h3>{topic.name}</h3>
            {selectedTopic === topic.id && (
              <p>{topic.description}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Study;
