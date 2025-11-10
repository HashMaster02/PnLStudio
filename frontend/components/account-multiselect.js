"use client";

import { useRef, useState, useEffect } from "react";
import { ChevronDown } from "lucide-react";

const AccountMultiSelect = ({ options, onChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedItems, setSelectedItems] = useState([]);
  const dropdownRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    setSelectedItems(options);
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSelectAll = (e) => {
    if (e.target.checked) {
      setSelectedItems(options);
      onChange({ accounts: options });
    } else {
      setSelectedItems([]);
      onChange({ accounts: [] });
    }
  };

  const handleSelect = (option) => {
    if (selectedItems.includes(option)) {
      const newSelections = selectedItems.filter((item) => item !== option);
      setSelectedItems(newSelections);
      onChange({ accounts: newSelections });
    } else {
      const newSelections = [...selectedItems, option];
      setSelectedItems(newSelections);
      onChange({ accounts: newSelections });
    }
  };

  return (
    <div className="relative w-80" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex w-full items-center justify-between rounded-lg border bg-white px-3 py-2 text-left text-sm "
      >
        <span className="truncate">
          {selectedItems.length > 0
            ? selectedItems.join(", ")
            : "Select accounts"}
        </span>
        <ChevronDown className="h-4 w-4 text-gray-500" />
      </button>

      {isOpen && (
        <div className="absolute mt-1 w-full rounded-md border border-gray-200 bg-white py-1 shadow-lg">
          <label className="flex cursor-pointer items-center px-3 py-2 hover:bg-gray-50">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              checked={selectedItems.length === options.length}
              onChange={handleSelectAll}
            />
            <span className="ml-2 text-sm text-gray-700">Select all</span>
          </label>

          {options.map((option) => (
            <label
              key={option}
              className="flex cursor-pointer items-center px-3 py-2 hover:bg-gray-50"
            >
              <input
                type="checkbox"
                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                checked={selectedItems.includes(option)}
                onChange={() => handleSelect(option)}
              />
              <span className="ml-2 text-sm text-gray-700">{option}</span>
            </label>
          ))}
        </div>
      )}
    </div>
  );
};

export default AccountMultiSelect;
