<script>
	import { user } from "./store.js";
</script>

<p><strong>
	{#if $user}
		You are logged in as <code>{$user.username}</code>.
	{:else}
		You are logged out. Create an account to start reviewing.
	{/if}
</strong></p>

<p>Harnessing the power of spaced repetition, our application empowers you
to absorb information and enhance your memory retention like never
before.</p>

<p>Spaced repetition is a learning technique backed by extensive research in
cognitive psychology. It involves reviewing material at gradually increasing
intervals, which has been shown to significantly improve long-term retention of
information. By using this approach, you're not just learning—you're retaining
knowledge for the long haul.</p>

<p>At Beedrill, we’ve integrated the innovative capabilities of GPT-3.5 to
streamline your study experience. Our app automatically generates tailored
flashcards from your input, simplifying the creation process and allowing you to
focus more on learning and less on preparation.</p>

<p>Here's what you can look forward to with Beedrill:</p>

<ul>
	<li>Automatically generated flashcards created by advanced GPT-3.5
	technology.</li>
	<li>A simple, effective spaced repetition system to optimize your study
	time.</li>
	<li>A user-friendly interface that makes learning seamless and
	engaging.</li>
</ul>

<p>Whether you’re cramming for exams, mastering new concepts, or just brushing
up on your knowledge, Beedrill is here to support your educational journey.
Start using our flashcard system today and experience a smarter way to
learn!</p>
