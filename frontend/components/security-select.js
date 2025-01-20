export function SecuritySelect({ value, tickers, onChange }) {
    const handleOnChange = (event) => {
        onChange({ security: event.target.value });
    };

    return (
        <select
            value={value}
            onChange={handleOnChange}
            className="w-full text-gray-900 text-sm border rounded-lg px-4 py-2 focus:outline-none"
        >
            {tickers.map((ticker) => (
                <option key={ticker}>{ticker}</option>
            ))}
        </select>
    );
}
