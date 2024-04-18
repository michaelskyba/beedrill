<script>
	import { reviewState } from "./store.js";
	import { get } from "svelte/store";

	function showBack() {
		const state = get(reviewState);
		state.step = "back";
		reviewState.set(state);
	}
</script>

{#if $reviewState.due_card_count == 1}
	<p>There is 1 cards left to review in {$reviewState.deck_name}.</p>
{:else}
	<p>There are {$reviewState.due_card_count} cards left to review in
	{$reviewState.deck_name}.</p>
{/if}

<blockquote>
	<h3>{$reviewState.card.front}</h3>
	<hr>
	{#if $reviewState.step == "front"}
		<h3>...</h3>
	{:else}
		<h3>{$reviewState.card.back}</h3>
	{/if}
</blockquote>

<hr>

{#if $reviewState.step == "front"}
	<div id="review">
		<button on:click={showBack}>Show back</button>
	</div>
{:else}
	<p>Did you correctly recall this card?</p>

	<div id="review">
		<button>Correct</button>
		<button>Incorrect</button>
	</div>
{/if}

<style>
	h3, p {
		text-align: center;
	}

	blockquote {
		padding: 2em;
	}

	hr {
		margin: 2em;
	}

	div#review {
		display: flex;
		justify-content: center;
		align-content: center;
		gap: 1em;
	}
</style>
