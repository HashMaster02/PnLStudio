const PLTabs = ({ selected, onChange }) => {
    const handleClick = (tab) => {
        onChange({
            pnl_type: tab.toLowerCase().split(' ').join('_'),
        });
    };

    const tablist = ['total', 'realized_total', 'unrealized_total'];
    const getLabel = {
        total: 'Total',
        realized_total: 'Realized Total',
        unrealized_total: 'Unrealized Total',
    };

    return (
        <div className="max-w-4xl mx-auto p-4">
            <div className="flex border-b">
                {tablist.map((tab) => (
                    <button
                        key={`${tab}_tab`}
                        onClick={() => handleClick(tab)}
                        className={`px-4 py-2 text-sm rounded-t-lg ${
                            getLabel[selected] === getLabel[tab]
                                ? 'border-t border-l border-r bg-white'
                                : 'text-gray-600 hover:text-gray-800'
                        }`}
                    >
                        {getLabel[tab]}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default PLTabs;
