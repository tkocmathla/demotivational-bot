# Demotivational Bot

Demotivational Bot is a GPT-2 model fine-tuned to generate demotivational poster quotes.

## Usage

Activate the pipenv environment to install dependencies.

```bash
$ cd bot
$ pipenv install
$ pipenv shell
```

### Fine tuning

Use the script from `gpt-2-simple` to fine-tune the model on titles and quotes from the demotivational posters on despair.com. 

```bash
$ gpt_2_simple --model_name 345M --steps 50 finetune ../demotivational_posters.txt
```

### Generating quotes

```bash
$ python src/bot.py generate --input-file ../demotivational_posters.txt --nsamples 25 --temperature 0.7 --k 20 --prefix Innovation
```