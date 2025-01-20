export function DateRangeSelect({ startDate, endDate, onChange }) {
    const handleStartOnChange = (event) => {
        onChange({ start_date: event.target.value, end_date: endDate });
    };

    const handleEndOnChange = (event) => {
        onChange({ end_date: event.target.value, start_date: startDate });
    };

    return (
        <div className="grid grid-cols-2 gap-4">
            <input
                type="date"
                value={startDate}
                onChange={handleStartOnChange}
                className="w-full text-gray-900 text-sm border rounded-lg px-4 py-2 focus:outline-none"
            />
            <input
                type="date"
                value={endDate}
                onChange={handleEndOnChange}
                className="w-full text-gray-900 text-sm border rounded-lg px-4 py-2 focus:outline-none"
            />
        </div>
    );
}
