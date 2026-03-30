import React from 'react';

type SportOption = {
  label: string;
  value: string;
};

type SportSelectorProps = {
  value: string;
  onChange: (value: string) => void;
  options?: SportOption[];
};

const defaultOptions: SportOption[] = [
  { label: 'Cycling Overall', value: 'cycling_overall' },
  { label: 'Road Cycling', value: 'Ride' },
  { label: 'Mountain Bike', value: 'MountainBikeRide' },
  { label: 'Gravel', value: 'GravelRide' },
  { label: 'Virtual Ride', value: 'VirtualRide' },
  { label: 'Run', value: 'Run' }
];

export default function SportSelector({ value, onChange, options }: SportSelectorProps) {
  const sportOptions = options ?? defaultOptions;

  return (
    <div className="form-block">
      <label htmlFor="sport" className="form-label">
        Sport
      </label>
      <select id="sport" className="select" value={value} onChange={(e) => onChange(e.target.value)}>
        {sportOptions.map((sport) => (
          <option key={sport.value} value={sport.value}>
            {sport.label}
          </option>
        ))}
      </select>
    </div>
  );
}
