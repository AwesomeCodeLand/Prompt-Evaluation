# style prompt

StylePrompt = """
Please analyze the part of speech of the following sentence and output in the format provided in the example:
"我今天早上吃的面包"

Example format: "代词\副词\名词\动词\名词"
End of example

Please convert the following sentence into the requested format:
{}
"""


GrammarPrompt_ZH = """
请理解下面这段话，然后按照语法流利度和内容准确性，以0-10为打分范围对内容进行打分。 语法越正确，分值越高。语法越错误，分值越低。 内容描述越清晰，分值越高。内容描述越不清晰，分值越低。
示例:
"我与父亲不相见已二年余了，我最不能忘记的是他的背影。那年冬天，祖母死了，父亲的差使也交卸了，正是祸不单行的日子，我从北京到徐州，打算跟着父亲奔丧回家。" 
打分结果:
{
    "score": 9.5,
    "reason": "语法正确，内容描述清晰。"
}

"朵朵 忍着臭气将垃圾桶 周围的垃圾清理干净。刚要动手看见。乐乐原地，不动了，正抓耳挠腮。若有所思。" 打分为1
{
    "score": 1.5,
    "reason": "语法错误，内容描述不清晰。"
}

请你理解示例后，为下面这段话进行打分。
{}
"""
GrammerPrompt_EN = """
Please understand the following paragraph and rate the content on a scale of 0-10 based on grammar fluency and content accuracy. The more correct the grammar, the higher the score. The more incorrect the grammar, the lower the score. The clearer the content description, the higher the score. The less clear the content description, the lower the score.
Example:
I haven't seen my father for over two years, and what I can't forget the most is his back. That winter, my grandmother died, and my father's mission was also handed over. It was a day when disaster never came alone. I went from Beijing to Xuzhou and planned to follow my father's funeral home
Scoring results:
{
    "score": 9.5,
    "Reason":" The grammar is correct and the content description is clear"
}
Duoduo endured the stench and cleaned up the garbage around the trash can. Just about to start seeing it, Lele was in place, not moving, scratching her ears and cheeks. Feeling thoughtful, the score was 1
{
    "score": 1.5,
    "Reason": "syntax error, unclear content description."
}
After understanding the example, please rate the following paragraph in the `` and use Chinese describe reason.
`{}`
"""
