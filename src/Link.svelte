<script>
	export let pageLinked;
	export let text;
	export let disabled = false;

	import { page } from "./store.js";

	const click = () => {
		page.set(pageLinked);
	}

	let buttonClass;
	page.subscribe(v => {
		buttonClass = v == pageLinked ? "active" : "inactive";
	})
</script>

{#if disabled}
	<button class={buttonClass} disabled>{text}</button>
{:else}
	<button class={buttonClass} on:click={click}>{text}</button>
{/if}

<style>
	button.active {
		background-color: white;
		color: black;
	}
</style>
