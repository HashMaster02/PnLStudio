import React from 'react';

export function TopDownList({ securities }) {
    return (
        <div className="rounded-xl border border-gray-200 ">
            <div className="bg-emerald-500 text-white px-4 py-2 rounded-t-xl">
                Top down
            </div>
            <div className="p-4 grid grid-cols-2 gap-4 place-items-center font-bold">
                <div className="text-gray-500">Ticker</div>
                <div className="text-gray-500">Value</div>
            </div>
            <div className="max-h-96 p-4 overflow-y-scroll">
                {securities ? (
                    <div className="grid grid-cols-2 gap-4 text-sm place-items-center">
                        {securities.map(({ security, value }) => (
                            <React.Fragment key={security}>
                                <p>{security}</p>
                                <p>${Math.trunc(value).toLocaleString()}</p>
                            </React.Fragment>
                        ))}
                    </div>
                ) : (
                    <h1 className="font-bold text-center">NO DATA</h1>
                )}
            </div>
        </div>
    );
}
