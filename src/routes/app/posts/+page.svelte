<script lang="ts">
	let { data } = $props();
</script>

<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
	{#each data.posts as post}
		<div class="flex flex-col rounded-xl border p-4">
			<h1 class="w-full border-b text-2xl font-bold">{post.title}</h1>
			<p class="mt-4">
				{post.body}
			</p>
		</div>
	{/each}
</div>
