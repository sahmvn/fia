<script lang="ts">
	import * as InputGroup from '$lib/components/ui/input-group/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import { handleError } from '$lib/consts.js';
	import { analyzeMovieScript, findMovieScripts } from '$lib/data.remote.js';
	import ArrowUpIcon from '@lucide/svelte/icons/arrow-up';
	import PlusIcon from '@lucide/svelte/icons/plus';
	import { toast } from 'svelte-sonner';

	let { data } = $props();

	let btnDisabled = $state(false);
	let query = $state('titanic');
	let options = $state<string[]>([]);

	async function localFindMovieScripts() {
		btnDisabled = true;
		try {
			const ops = await findMovieScripts({ query });
			options = ops;
			console.log(options);
		} catch (err) {
			handleError(err);
		}
		btnDisabled = false;
	}

	async function localAnalyzeMovieScripts(scriptUrl: string) {
		btnDisabled = true;
		try {
			const script = await analyzeMovieScript({ scriptUrl });
			console.log(script);
			toast.success('Success');
		} catch (err) {
			handleError(err);
		}
		btnDisabled = false;
	}
</script>

<div class="mx-auto flex h-full w-full max-w-3xl flex-col items-center justify-center">
	<h1 class="text-4xl font-semibold">SOME NICE TEXT</h1>
	<InputGroup.Root class="mt-8">
		<InputGroup.Textarea bind:value={query} placeholder="Ask, Search or Chat..." />
		<InputGroup.Addon align="block-end">
			<!-- <InputGroup.Text class="ml-auto">52% used</InputGroup.Text> -->
			<!-- <Separator orientation="vertical" class="!h-4" /> -->
			<InputGroup.Button
				variant="default"
				class="ml-auto cursor-pointer rounded-full"
				size="icon-xs"
				onclick={localFindMovieScripts}
				disabled={btnDisabled}
			>
				<ArrowUpIcon />
				<span class="sr-only">Send</span>
			</InputGroup.Button>
		</InputGroup.Addon>
	</InputGroup.Root>
	<div class="mt-5 flex flex-col">
		{#each options as script}
			<button
				disabled={btnDisabled}
				onclick={async () => await localAnalyzeMovieScripts(script)}
				class="cursor-pointer">{script}</button
			>
		{/each}
	</div>
</div>
