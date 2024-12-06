import React from 'react';
import './styles/DeveloperCard.css'; // Custom CSS for styling the card

const DeveloperCard = ({ name, description, skills, image }) => {
  return (
    <div className="developer-card">
      <img src={image} alt={`${name}'s photo`} className="developer-photo" />
      <h3>{name}</h3>
      <h4>Backend Developer</h4> {/* Added Backend Developer heading */}
      <p>{description}</p>
      <h4>Skills</h4>
      <ul>
        {skills.map((skill, index) => (
          <li key={index}>{skill}</li>
        ))}
      </ul>
    </div>
  );
};

export default DeveloperCard;
