"use client";
import { useState, useEffect } from "react";
import { MetricCards } from "@/components/metric-cards";
import { PLChart } from "@/components/pl-chart";
import { BottomUpList } from "@/components/bottom-up-list";
import { TopDownList } from "@/components/top-down-list";
import { SecuritySelect } from "@/components/security-select";
import { DateRangeSelect } from "@/components/date-range-select";
import AccountMultiSelect from "@/components/account-multiselect";
import Menu from "@/components/menu";
import {
  fetchCardData,
  fetchTopDownBottomUpData,
  fetchAccountsData,
  fetchSecuritiesData,
  fetchGraphData,
} from "@/data/fetching";

export default function Home() {
  const [filters, setFilters] = useState({
    accounts: [""],
    security: "",
    start_date: "",
    end_date: "",
    pnl_type: "",
  });

  const [cardData, setCardData] = useState(null);
  const [topDownBottomUpData, setTopDownBottomUpData] = useState(null);
  const [accountsData, setAccountsData] = useState(null);
  const [securitiesData, setSecuritiesData] = useState(null);
  const [graphData, setGraphData] = useState(null);

  const fetchAllData = async (newFilters) => {
    try {
      const updatedFilters = { ...filters, ...newFilters };
      setFilters(updatedFilters);

      const card = await fetchCardData(updatedFilters);
      const tdbu = await fetchTopDownBottomUpData(updatedFilters);
      const graph = await fetchGraphData(updatedFilters);

      setCardData(card);
      setTopDownBottomUpData(tdbu);
      setGraphData(graph);
    } catch (error) {
      console.log(error);
    }
  };

  const refreshGraph = async (newFilters) => {
    try {
      const updatedFilters = { ...filters, ...newFilters };
      setFilters(updatedFilters);

      const graph = await fetchGraphData(updatedFilters);

      setGraphData(graph);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    async function initialLoad() {
      const accounts = await fetchAccountsData();
      const securities = await fetchSecuritiesData();
      const updatedFilters = {
        ...filters,
        ...{
          accounts: accounts.data,
          security: securities.data[0],
          start_date: "2024-01-01",
          end_date: "2024-12-20",
          pnl_type: "total",
        },
      };
      setFilters(updatedFilters);
      await fetchAllData(updatedFilters);

      const graph = await fetchGraphData(updatedFilters);
      setAccountsData(accounts);
      setSecuritiesData(securities);
      setGraphData(graph);
    }

    initialLoad();
  }, []);

  return (
    <>
      <Menu />
      <main className="container mx-auto p-4 space-y-4 font-inter">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div className="rounded-xl border border-gray-200 p-4 space-y-6">
            <SecuritySelect
              items={
                securitiesData && securitiesData.data ? securitiesData.data : []
              }
              onChange={fetchAllData}
            />
            <DateRangeSelect
              startDate={filters.start_date}
              endDate={filters.end_date}
              onChange={fetchAllData}
            />
          </div>
          <div className="rounded-xl border border-gray-200 p-4">
            <AccountMultiSelect
              options={
                accountsData && accountsData.data ? accountsData.data : []
              }
              onChange={fetchAllData}
            />
          </div>
        </div>
        <MetricCards data={cardData?.data ? cardData.data : null} />
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
          <PLChart
            pnltype={filters.pnl_type}
            data={graphData && graphData.data ? graphData.data : null}
            onChange={refreshGraph}
          />
          <TopDownList
            securities={
              topDownBottomUpData && topDownBottomUpData.data
                ? topDownBottomUpData.data.top_down
                : []
            }
          />
          <BottomUpList
            securities={
              topDownBottomUpData && topDownBottomUpData.data
                ? topDownBottomUpData.data.bottom_up
                : []
            }
          />
        </div>
      </main>
    </>
  );
}
