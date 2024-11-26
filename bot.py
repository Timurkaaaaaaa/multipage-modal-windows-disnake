import disnake
from disnake.ext import commands
from disnake import AllowedMentions
from disnake.ext.commands import Bot
from disnake import TextInputStyle
import sqlite3


connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Answers (
id TEXT,
answer TEXT,
question TEXT
)
''')
connection.commit()


bot = commands.Bot()





@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.slash_command()
async def mulipage_modal(inter):
    await inter.response.send_message(
        "Press the button to open a modal window",
        components = [
            disnake.ui.Button(label="multipage modal window", style=disnake.ButtonStyle.success, custom_id="open")
                ])


@bot.listen("on_button_click")
async def help_listener(inter: disnake.MessageInteraction):
    if inter.component.custom_id == "open":
        await inter.response.send_modal(modal=page_one())
    else:
        return

class page_one(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Question 1:",
                placeholder="Example...",
                custom_id="Question 1:",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Question 2:",
                placeholder="Example...",
                custom_id="Question 2:",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Question 3:",
                placeholder="Example...",
                custom_id="Question 3:",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Question 4:",
                placeholder="Example...",
                custom_id="Question 4:",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Question 5:",
                placeholder="Example...",
                custom_id="Question 5:",
                style=TextInputStyle.short,
                max_length=50,
            ),
        ]
        super().__init__(title="Modal Window | Page 1/2", components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        user_id = str(inter.author.id)
        for key, value in inter.text_values.items():
            cursor.execute(
            "INSERT INTO Answers (id, answer, question) VALUES (?, ?, ?)",
            (user_id, value[:1024], key.capitalize())
        )
            connection.commit()
        await inter.response.send_message(
            "Press the button to go to the next page",
            ephemeral=True,
            components = [
                disnake.ui.Button(label="multipage modal window", style=disnake.ButtonStyle.success, custom_id="open2")
                ])

@bot.listen("on_button_click")
async def help_listener(inter: disnake.MessageInteraction):
    if inter.component.custom_id == "open2":
        await inter.response.send_modal(modal=page_two())
    else:
        return

class page_two(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Question 6:",
                placeholder="Example...",
                custom_id="Question 6:",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Question 7:",
                placeholder="Example...",
                custom_id="Question 7:",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Question 8:",
                placeholder="Example...",
                custom_id="Question 8:",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Question 9:",
                placeholder="Example...",
                custom_id="Question 9:",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Question 10:",
                placeholder="Example...",
                custom_id="Question 10:",
                style=TextInputStyle.short,
                max_length=50,
            ),
        ]
        super().__init__(title="Modal Window | Page 2/2", components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="Modal Window")
        user_id = str(inter.author.id)
        for key, value in inter.text_values.items():
            cursor.execute(
            "INSERT INTO Answers (id, answer, question) VALUES (?, ?, ?)",
            (user_id, value[:1024], key.capitalize())
        )
            connection.commit()
        cursor.execute("SELECT answer, question FROM Answers WHERE id = '" + user_id +"'")
        results = cursor.fetchall()
        cursor.execute("SELECT COUNT(Answer) FROM Answers WHERE id = '" + user_id +"'")
        count = cursor.fetchone()[0]
        for i in range(count):
            result = results[i]
            embed.add_field(
                name=result[1],
                value=result[0],
                inline=False,
            )
        cursor.execute("DELETE FROM Answers WHERE id = '" + user_id +"'")
        connection.commit()
        await inter.response.send_message(embed=embed)



bot.run("YOUR TOKEN")

connection.close()
