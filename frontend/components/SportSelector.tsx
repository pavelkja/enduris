import React from 'react';

type SportSelectorProps = {
  value: string;
  onChange: (value: string) => void;
};

const sportOptions = [
  { label: 'cycling_overall', value: 'cycling_overall' },
  { label: 'ride', value: 'ride' },
  { label: 'run', value: 'run' }
];

export default function SportSelector({ value, onChange }: SportSelectorProps) {
  return (
    <div>
      <label htmlFor="sport" style={{ display: 'block', marginBottom: 8 }}>
        Sport
      </label>
      <select id="sport" value={value} onChange={(e) => onChange(e.target.value)}>
        {sportOptions.map((sport) => (
          <option key={sport.value} value={sport.value}>
            {sport.label}
          </option>
        ))}
      </select>
    </div>
  );
}
