import { useState, useRef, useEffect } from 'react';
import { ChevronDown } from 'lucide-react';

export function SecuritySelect({ value, items, onChange }) {
	const [isOpen, setIsOpen] = useState(false);
	const [searchTerm, setSearchTerm] = useState('');
	const [selectedItem, setSelectedItem] = useState('');
	const dropdownRef = useRef(null);

	// const items = ['One', 'Two', 'Three', 'Four', 'Five'];

	const filteredItems = items.filter(item =>
		item.toLowerCase().includes(searchTerm.toLowerCase())
	);

	const handleItemSelect = item => {
		setSelectedItem(item);
		onChange({ security: item });

		setIsOpen(false);
		setSearchTerm('');
	};

	useEffect(() => {
		function handleClickOutside(event) {
			if (
				dropdownRef.current &&
				!dropdownRef.current.contains(event.target)
			) {
				setIsOpen(false);
			}
		}

		document.addEventListener('mousedown', handleClickOutside);
		return () =>
			document.removeEventListener('mousedown', handleClickOutside);
	}, []);

	return (
		<div className="relative w-[300px]" ref={dropdownRef}>
			{/* Dropdown Button */}
			<button
				onClick={() => setIsOpen(!isOpen)}
				className="text-sm flex items-center justify-between w-full px-4 py-2 border rounded-lg text-grey-900 focus:outline-none"
			>
				<span>{selectedItem}</span>
				<ChevronDown className="w-4 h-4" />
			</button>

			{/* Dropdown Menu */}
			{isOpen && (
				<div className="absolute z-100 w-full mt-1 bg-white rounded-md shadow-lg">
					{/* Search Input */}
					<div className="p-2">
						<input
							type="text"
							placeholder="Search..."
							value={searchTerm}
							onChange={e => setSearchTerm(e.target.value)}
							className="w-full px-3 py-2 text-gray-900 bg-transparent rounded-md focus:outline-none"
						/>
					</div>

					{/* Items List */}
					<div className="max-h-60 overflow-auto">
						{filteredItems.map(item => (
							<label
								key={item}
								className={`flex items-center px-4 py-2 cursor-pointer ${
									selectedItem === item
										? 'bg-blue-600'
										: 'hover:bg-blue-600'
								}`}
							>
								<div className="relative flex items-center">
									<input
										type="radio"
										name="dropdown-item"
										checked={selectedItem === item}
										onChange={() => handleItemSelect(item)}
										className="appearance-none w-4 h-4 border-2 border-blue-500 rounded bg-transparent checked:bg-blue-500 checked:border-blue-500"
									/>
									<svg
										className={`absolute w-4 h-4 pointer-events-none ${
											selectedItem === item
												? 'text-white'
												: 'hidden'
										}`}
										viewBox="0 0 17 12"
										fill="none"
										stroke="currentColor"
										strokeWidth="2"
										strokeLinecap="round"
										strokeLinejoin="round"
									>
										<path d="M1 4.5L5.5 9L15 1" />
									</svg>
								</div>
								<span className="text-gray-900 ml-2">
									{item}
								</span>
							</label>
						))}
					</div>
				</div>
			)}
		</div>
	);
}
