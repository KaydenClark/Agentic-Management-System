// Registers tsx-hooks.mjs so a render test can `await import()` app modules.
import { register } from 'node:module';

register('./tsx-hooks.mjs', import.meta.url);
