import re,asyncio
import package.paypaypublic as ppub
import discord #今回はdiscord.py V2を使うことにする。
#discord.py V2だからな！
#pip install git+https://github.com/Rapptz/discord.py
from discord import app_commands
from discord.ui import Modal,text_input
token="token"#BotのTokenを入力。


intents = discord.Intents.default()
intents.message_content=True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)




@client.event
async def on_ready():
    print("起動。")
    await tree.sync()
#
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    if re.search(r'https://pay.paypay.ne.jp',message.content) :
        p_link=re.findall(r'https://pay.paypay.ne.jp/+\w+\w',message.content)[0].replace("https://pay.paypay.ne.jp/","")
        print(p_link)
        c_channel = message.channel
        c_author=message.author
        def check(m):
            return m.author == c_author and m.channel == c_channel
        pcode_umu=ppub.check_pcode(p_link)
        if pcode_umu=="SUCCESS":
                await message.channel.send("使用済リンクです。")
                return
        elif pcode_umu=="Cannot find P2P link":
            await message.channel.send("受け取りリンクが見つかりません。")
            return
        elif pcode_umu=="パスワード付き":
            await message.channel.send("パスワード付きリンクを検知しました。"+'\n'+"20秒以内に半角で4桁のパスワードを入力してください    例:0417"+'\n'+"これを拒否する場合は拒否と入力してください。")
            try:
                msg = await client.wait_for('message',check=check,timeout=20)
                if msg.content=="拒否":
                    await message.channel.send("拒否されました。")
                    return
                    
                try:
                    ererer=int(msg.content)
                except:
                    await message.channel.send("無効なパスワードです。")
                    return

                pcode_data=(msg.content)
            except asyncio.TimeoutError:
                await message.channel.send("タイムアウトしました。")
                return
        elif pcode_umu=="パスワード無し":
            pcode_data="1919"
                
        jido_kessai=ppub.start(p_link,pcode_data)
        try:
            dataaaaaa=jido_kessai[0]
            if type(jido_kessai)==list:uketori_st=True
            else:uketori_st=False
        except:uketori_st=False
        if uketori_st == True:
            embed = discord.Embed( # Embedを定義する
                        title=f"{jido_kessai[0]}さんから受け取り",# タイトル
                        description=f"金額:{jido_kessai[2]}円",
                        color=0x00ff00
                        )
            embed.set_thumbnail(url=jido_kessai[1])
            await message.channel.send(embed=embed)






class Md(Modal):
    a = text_input.TextInput(label='PayPay受け取りリンク', placeholder='https://pay.paypay.ne.jp/HAudjw45', max_length=35, required=True)
    b = text_input.TextInput(label='パスコード', style=discord.TextStyle.short, required=True,max_length=4,placeholder="1234")
    def __init__(self):
        super().__init__(title='PayPay受け取り')

    async def on_submit(self, interaction:discord.Interaction):
        paypay_link=self.a.value.replace("https://pay.paypay.ne.jp/","")
        paypay_passcode=self.b.value
        pcode_umu=ppub.check_pcode(paypay_link)
        if pcode_umu=="Cannot find P2P link":
            await interaction.response.send_message("そのPayPayリンクは存在しません。",ephemeral=True)
            return
        #pp_author=interaction.user
        uketori=ppub.start(paypay_link,paypay_passcode)
        #めんどくさかったので簡単に。
        try:
            dataaaaaa=uketori[0]
            if type(uketori)==list:uketori_st=True
            else:uketori_st=False
        except:uketori_st=False
        if uketori_st == True:
            embed = discord.Embed( # Embedを定義する
                        title=f"{uketori[0]}さんから受け取り",# タイトル
                        description=f"金額:{uketori[2]}円",
                        color=0x00ff00
                        )
            embed.set_thumbnail(url=uketori[1])
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            if uketori=="パスコードが違います":
                await interaction.response.send_message("失敗しました。パスコードが間違っていました。お金は2日ほど後に返ってくるのでご安心ください。",ephemeral=True)
            else:
                print(uketori)
                await interaction.response.send_message("失敗しました。リンクが不正だったり、システムエラーが起きていたりしている可能性があります。",ephemeral=True)
        




@tree.command(name="send_paypay",description="PayPayリンクを送って支援できます。")
async def test(interaction: discord.Interaction):
    await interaction.response.send_modal(Md())


client.run(token)
