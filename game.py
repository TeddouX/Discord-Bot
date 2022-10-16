from utils import check_reaction

from discord.ext import commands
import discord

class Game:
    def __init__(self) -> None:
        # Directions
        self.up = '⬆️'
        self.down = '⬇️'
        self.left = '⬅️'
        self.right = '➡️'

        # Tiles
        self.black_tile = '🔲'
        self.player_tile = '🙂'
        self.enemy_tile = '😡'

        self.size = 6
        self.player_pos = [3, 3]
        self.is_running = True
    
    async def generate_board(self, ctx: commands.context.Context) -> discord.message.Message:
        final_message = ''
        for x in range(self.size):
            for y in range(self.size):
                if [y+1, x+1] == self.player_pos:
                    final_message += self.player_tile
                else: final_message += self.black_tile
            final_message += '\n'

        message = await ctx.send(final_message)

        await message.add_reaction(self.up)
        await message.add_reaction(self.down)
        await message.add_reaction(self.left)
        await message.add_reaction(self.right)

        return message

    async def update_movement(self, game_message: discord.message.Message) -> None:
        for i in game_message.reactions:
            if i.emoji == self.up and i.count >= 2:
                self.move_player([0, -1])
            elif i.emoji == self.down and i.count >= 2:
                self.move_player([0, 1])
            elif i.emoji == self.left and i.count >= 2:
                self.move_player([-1, 0])
            elif i.emoji == self.right and i.count >= 2:
                self.move_player([1, 0])

    def move_player(self, move_vector: list) -> None:
        self.player_pos[0] += move_vector[0]
        self.player_pos[1] += move_vector[1]

    async def update_board(self, ctx: commands.context.Context, game_message: discord.message.Message) -> None:
        try:
            has_reacted = False
            while not has_reacted:
                has_reacted = check_reaction(ctx, [self.up, self.down, self.left, self.right])
        except discord.NotFound or discord.HTTPException:
            await ctx.send('The game ended unexpectedly')
            self.is_running = False

        await game_message.delete()
        if self.is_running == True:
            new_message = await self.generate_board(ctx)
            await self.update_board(ctx, new_message)

    async def start(self, ctx: commands.context.Context) -> None:
        message = await self.generate_board(ctx)
        await self.update_board(ctx, message)