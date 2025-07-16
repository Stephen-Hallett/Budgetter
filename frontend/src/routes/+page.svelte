<script lang="ts">
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Select, SelectTrigger, SelectContent, SelectItem } from '$lib/components/ui/select';
	import { Badge } from '$lib/components/ui/badge';
	// You might need to import Button if you use it elsewhere

	const filters = ['Food', 'Lifestyle', 'Subscriptions'];
	const segments = [
		{ name: 'Food', color: 'bg-green-200', percent: 50 },
		{ name: 'Lifestyle', color: 'bg-yellow-200', percent: 30 },
		{ name: 'Subscriptions', color: 'bg-purple-200', percent: 20 },
		{ name: 'Fitness', color: 'bg-orange-200', percent: 0 }
	];
	const transactions = [
		{
			amount: '$30.20',
			category: 'Food',
			color: 'bg-green-100',
			name: 'Transaction Name',
			particulars: 'date - particulars'
		},
		{
			amount: '$10.00',
			category: 'Food',
			color: 'bg-green-100',
			name: 'Transaction Name',
			particulars: 'date - particulars'
		},
		{
			amount: '$19.99',
			category: 'Subscriptions',
			color: 'bg-purple-100',
			name: 'Transaction Name',
			particulars: 'date - particulars'
		},
		{
			amount: '$15.00',
			category: 'Lifestyle',
			color: 'bg-yellow-100',
			name: 'Transaction Name',
			particulars: 'date - particulars'
		},
		{
			amount: '$120.50',
			category: 'Food',
			color: 'bg-green-100',
			name: 'Transaction Name',
			particulars: 'date - particulars'
		}
	];
</script>

<div class="mx-auto min-h-screen max-w-6xl rounded-[60px] border bg-white p-8">
	<h1 class="mb-8 text-center text-4xl font-bold">Budgetter</h1>

	<!-- Filters Bar -->
	<Card class="mb-8 rounded-2xl">
		<CardContent class="flex flex-wrap items-center gap-6 py-6">
			<div class="flex items-center gap-2">
				<span class="font-semibold">Time:</span>
				<Select>
					<SelectTrigger class="w-[100px]"></SelectTrigger>
					<SelectContent>
						<SelectItem value="jan">Jan</SelectItem>
						<SelectItem value="feb">Feb</SelectItem>
						<!-- more options -->
					</SelectContent>
				</Select>
				<Select>
					<SelectTrigger class="w-[100px]">To</SelectTrigger>
					<SelectContent>
						<SelectItem value="mar">Mar</SelectItem>
						<SelectItem value="apr">Apr</SelectItem>
						<!-- more options -->
					</SelectContent>
				</Select>
			</div>
			<div class="flex items-center gap-2">
				<span class="font-semibold">Filters:</span>
				{#each filters as filter}
					<Badge class="border-red-300 bg-red-100 text-red-800">{filter}</Badge>
				{/each}
				<Select>
					<SelectTrigger class="w-[140px]">More</SelectTrigger>
					<SelectContent>
						<SelectItem value="subscriptions">Subscriptions</SelectItem>
						<!-- more options -->
					</SelectContent>
				</Select>
			</div>
		</CardContent>
	</Card>

	<!-- Main Content -->
	<div class="flex gap-6">
		<!-- Transactions List -->
		<Card class="flex-1 rounded-3xl">
			<CardContent class="py-6">
				<h2 class="mb-4 text-center text-2xl font-semibold">Transactions</h2>
				<div class="flex flex-col gap-4">
					{#each transactions as txn}
						<div
							class="flex items-center gap-4 rounded-lg border p-4 {txn.color}"
							style="border-left: 8px solid;"
						>
							<div class="w-28 text-2xl font-bold">{txn.amount}</div>
							<div class="flex-1">
								<div class="font-semibold">{txn.name}</div>
								<div class="text-sm text-gray-500">{txn.particulars}</div>
							</div>
							<Select>
								<SelectTrigger class="w-[120px]">
									{txn.category}
								</SelectTrigger>
								<SelectContent>
									<SelectItem value="food">Food</SelectItem>
									<SelectItem value="lifestyle">Lifestyle</SelectItem>
									<SelectItem value="subscriptions">Subscriptions</SelectItem>
								</SelectContent>
							</Select>
						</div>
					{/each}
				</div>
			</CardContent>
		</Card>

		<!-- Segments / Pie / Stats -->
		<div class="flex w-[380px] flex-col gap-6">
			<!-- Segments -->
			<Card class="rounded-3xl">
				<CardContent class="py-6">
					<h3 class="mb-4 text-lg font-semibold">Segments</h3>
					<ul>
						{#each segments as seg}
							<li class="mb-2 flex items-center gap-2">
								<span class={`inline-block h-4 w-4 rounded-full ${seg.color}`}></span>
								<span>{seg.name} - {seg.percent} %</span>
							</li>
						{/each}
					</ul>
				</CardContent>
			</Card>
			<!-- Donut Chart (placeholder) -->
			<Card class="flex h-60 items-center justify-center rounded-3xl">
				<span class="text-gray-400">[Pie Chart Here]</span>
				<!-- Use a chart library for real chart -->
			</Card>
			<!-- Stat Boxes -->
			<div class="flex gap-4">
				<Card class="flex-1 rounded-xl py-6 text-center">
					<div class="text-2xl font-bold">$378.20</div>
					<div class="text-gray-500">You Spent</div>
				</Card>
				<Card class="flex-1 rounded-xl py-6 text-center">
					<div class="text-2xl font-bold">47.21%</div>
					<div class="text-gray-500">Of Monthly Income</div>
				</Card>
			</div>
		</div>
	</div>
</div>
