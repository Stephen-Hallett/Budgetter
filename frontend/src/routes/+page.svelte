<script lang="ts">
  import { writable } from "svelte/store";
  import DonutChart from "../lib/DonutChart.svelte";

  // Mock data for demonstration
  let transactions = writable([
    {
      id: "trans_1",
      date: "2025-07-01",
      description: "Coffee",
      amount: -4.5,
      segment: "Food",
    },
    {
      id: "trans_2",
      date: "2025-07-02",
      description: "Groceries",
      amount: -50,
      segment: "Food",
    },
    {
      id: "trans_3",
      date: "2025-07-03",
      description: "Gym",
      amount: -30,
      segment: "Lifestyle",
    },
    {
      id: "trans_4",
      date: "2025-07-04",
      description: "Salary",
      amount: 2000,
      segment: "Income",
    },
    // ...more transactions
  ]);

  let page = 1;
  let pageSize = 10;
  let total = 30; // mock total

  // Mock segment proportions
  let segmentProportions = { Lifestyle: 0.5, Food: 0.5 };

  // Pagination logic
  $: paginatedTransactions = $transactions.slice(
    (page - 1) * pageSize,
    page * pageSize
  );

  function nextPage() {
    if (page * pageSize < total) page++;
  }
  function prevPage() {
    if (page > 1) page--;
  }
</script>

<div class="dashboard">
  <section class="left">
    <h2>Transactions</h2>
    <ul class="transactions">
      {#each paginatedTransactions as t}
        <li class="transaction">
          <div><strong>{t.description}</strong></div>
          <div>{t.date} | {t.amount} | {t.segment}</div>
        </li>
      {/each}
    </ul>
    <div class="pagination">
      <button on:click={prevPage} disabled={page === 1}>Previous</button>
      <span>Page {page}</span>
      <button on:click={nextPage} disabled={page * pageSize >= total}
        >Next</button
      >
    </div>
  </section>
  <section class="right">
    <DonutChart {segmentProportions} />
  </section>
</div>

<style>
  .dashboard {
    display: flex;
    height: 100vh;
  }
  .left {
    flex: 1;
    padding: 2rem;
    overflow-y: auto;
    border-right: 1px solid #eee;
  }
  .right {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .transactions {
    list-style: none;
    padding: 0;
  }
  .transaction {
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #eee;
  }
  .pagination {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
  }
</style>
