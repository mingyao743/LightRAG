GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "Chinese"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "person", "geo", "event"]

PROMPTS["entity_extraction"] = """-目标-
针对可能与此活动相关的文本文档和实体类型列表，从文本中识别出所有此类实体，并识别出所有已识别实体之间的关系。
使用中文作为输出语言。

-步骤-1. 识别所有实体。对于每个识别出的实体，提取以下信息：
- entity_name：实体名称，使用中文。
- entity_type：以下类型之一：[{entity_types}]
- entity_description：实体属性和活动的全面描述
将每个实体格式化为 ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. 从步骤1中识别出的实体中，找出所有（源实体，目标实体）对，它们之间显然存在关联。
对于每个相关的实体对，提取以下信息：
- 源实体：如步骤1中所识别出的，源实体的名称
- 目标实体：如步骤1中所识别出的，目标实体的名称
- 关系描述：解释您认为源实体和目标实体之间存在关联的原因
- 关系强度：表示源实体和目标实体之间关系强度的数字评分
- 关系关键词：一个或多个高级关键字，概述了关系的总体性质，侧重于概念或主题，而不是具体细节
将每个关系格式化为 ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. 找出能够概括整个文本主要概念、主题或话题的高级关键词。这些关键词应能捕捉文档中所包含的总体思想。
将内容级关键词以("content_keywords"{tuple_delimiter}<high_level_keywords>)的格式进行格式化。

4. 将步骤1和2中识别出的所有实体和关系以中文的形式作为单一列表输出。使用 **{record_delimiter}** 作为列表分隔符。

5. 当完成后，输出 {completion_delimiter}

######################
-示例-
######################
{examples}

#############################
-真实数据-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
输出：
"""

PROMPTS["entity_extraction_examples"] = [
    """示例 1:

Entity_types: [person, role, organization, event, location, concept, date]

Text:
利率水平的变化和贷款的难易程度对个人资产和生活方式的影响\n对于大多数家庭来说，利率水平对资产有着深远的影响。在美国，数十年来许多家庭习惯于通过贷款的方式来实现他们的梦想，这产生的影响体
现在每个月的家庭账单中。遗憾的是，对于大多数家庭来说，日积月累的巨大债务和他们的偿还能力并不匹配，因此产生了不可估量的负面影响。其中最坏的影响莫过于宽松的信贷条件、资产管理的疏忽、收入水平与偿还能力不匹配而
造成的住宅抵押品的赎回权取消（见图1-2）。\n\n图1-2　房屋没收拍卖占总贷款的比例\n资料来源：Mortgage Bankers Association.\n过去数十年来个人贷款的迅速膨胀是一种文化现象，除了上述提到的几个原因，人口分布也是另>一个重要原因。婴儿潮出生的一代人（特指生于1946~1964年的人）疯狂地利用贷款，来购买喜爱的商品和服务。这场狂欢一直持续到金融危机爆发的2007年，这时贷款的“水龙头”开始关闭了。在新标准下，消费开始有所收敛，存款利>率逐渐上升（见图1-3）。减少债务成为人们新的口头禅，而不再是“记在我账上！”\n无论是什么导致了贷款的迅速上升，事实上，家庭的平均未偿还贷款额超过了其他任何一种贷款额度。表1-1列出了家庭没有能力偿还的巨大的贷款数
额。需要注意的是，这一额度的减少是随着去杠杆化潮流的推动而发生的。\n表1-1　家庭负债表（2009年12月）　（单位：10亿美元）\n\n如表1-1所示，未偿还的抵押房贷超过了任何一种贷款。这很清楚地表明了利率对家庭资产的影
响最大限度地体现在抵押房贷利率上。抵押房贷利率直接影响着每个家庭的月度收支状况。我相信读者大多数会有切身体会，并且意识到可调整的抵押房贷利率的变化对美国大多数家庭会产生的巨大影响。许多家庭都被所谓的“引诱利>率”哄骗走上了抵押贷款的不归路。自从2004年6月联邦储备系统进行一系列的利率上调之后，抵押房贷利率也随之上浮，繁重的抵押贷款使很多家庭不堪重负（见图1-2）。\n\n图1-3　今天，“记在我账上！”不再是口头禅\n资料来源：
Bureau of Economic Analysis and Haver Analytics.\n从中我们可以直接得知追踪利率变化的重要性，也可以了解许多年前影响利率上升或者下降的因素。\n1989年，也就是我开始在债券市场的职业生涯的前一年，我购买了我的第一
套房子。那年对我来说是特别的一年，我是如此兴奋，因为我实现了拥有一套房子的美国梦。\n虽然房子本身带来的都是骄傲和满足，但当时我并没有意识到与之对应的财务问题。当时我的贷款抵押利率高达惊人的11.25%，这是当时的
利率。我并没有过多地考虑利率的问题，因为我像其他21世纪初的人们一样，认为房价会一直上升，上升的房价可以抵消利率带来的额外成本。我所犯的错误和后来数百万其他人犯的错误一模一样。\n我最初的判断真是错得离谱！当我
逐渐意识到这一点时，美联储正在进行一场放缓经济运行速度的调整，其目的在于降低通货膨胀，使房地产市场的价格泡沫破灭。美联储升息的措施不仅给了我，更是给了在经济危机期间像我一样的“房奴”双重打击：我在高额的抵押贷
款上骑虎难下，房价随着房地产价格泡沫的破灭更是一落千丈。\n随着房地产价格泡沫的破灭，我房子的价格迅速下降了25%。数年来我一直试图再融资，但没有银行愿意考虑答应我的贷款请求，因为我的房子只能作为负资产进行抵押>。因此，我举步维艰。年复一年，我一直为这次失败的房屋投资负担着高额的抵押贷款。\n当时我一无所知，现在终于明白是什么。作为刚刚涉足贷款的人来说，我意识到贷款利率是如此重要，在面对相对来说较高的利率或者和我的收
入相比较高的利率时一定要三思而后行。我再也不会做出如此草率的、不计后果的借贷决定了。这意味着我需要更加关注债券市场。跟随债券市场的脚步能够帮助我制订更周全的计划，进行更有益的决策。最近的金融危机也给我上了很
好的一课：如果在信贷龙头收紧时再融资比较困难，那么对这类债务要保持机警，最好不要去承担。\n我还明白了“永远不要和美联储作对”这句谚语的真正含义。美联储对于整体经济和金融市场有着不可估量的影响，也会影响到我自己
的财富能否得到保障。无论怎么强调这一点的重要性都是不为过的。在第6章我们会深入讨论美联储这种巨大力量的重要性。\n最终我反败为胜了。那是在抵押贷款利率达到21世纪新低的时候，我从负担着最高抵押利率的人摇身一变，>开始负担最低的抵押利率。通过和债券市场亦步亦趋，我学会了在利率下跌时进行投机。而且，通过密切观察美联储的一举一动，我总是可以站在投资和经济运行的制高点。\n各位，请和我一样紧紧跟随债券市场的脚步，并且请将图1-1深深印在脑海里。让它时时刻刻提醒你债券市场对你的个人财富的影响有多么巨大。
################
Output:
("entity"{tuple_delimiter}利率水平{tuple_delimiter}concept{tuple_delimiter}影响个人资产和生活方式的重要因素，与贷款难易程度相关){record_delimiter}
("entity"{tuple_delimiter}贷款{tuple_delimiter}concept{tuple_delimiter}家庭实现梦想的手段，与利率水平和个人资产有直接关系){record_delimiter}
("entity"{tuple_delimiter}美国{tuple_delimiter}location{tuple_delimiter}文中提到的国家，许多家庭通过贷款实现梦想){record_delimiter}
("entity"{tuple_delimiter}金融危机{tuple_delimiter}event{tuple_delimiter}2007年发生的事件，导致贷款“水龙头”开始关闭){record_delimiter}
("entity"{tuple_delimiter}存款利率{tuple_delimiter}concept{tuple_delimiter}与消费和贷款有关，新标准下逐渐上升){record_delimiter}
("entity"{tuple_delimiter}家庭负债表{tuple_delimiter}concept{tuple_delimiter}表1-1中列出的家庭未偿还贷款额，反映家庭负债情况){record_delimiter}
("entity"{tuple_delimiter}抵押房贷{tuple_delimiter}concept{tuple_delimiter}家庭负债表中未偿还额最大的贷款类型，直接影响家庭月度收支){record_delimiter}
("entity"{tuple_delimiter}联邦储备系统{tuple_delimiter}organization{tuple_delimiter}美国中央银行，通过调整利率影响经济和贷款市场){record_delimiter}
("entity"{tuple_delimiter}债券市场{tuple_delimiter}concept{tuple_delimiter}作者职业生涯开始的地方，与利率变化紧密相关){record_delimiter}
("entity"{tuple_delimiter}1989年{tuple_delimiter}date{tuple_delimiter}作者购买第一套房子的年份，当时利率高达11.25%){record_delimiter}
("entity"{tuple_delimiter}21世纪初{tuple_delimiter}date{tuple_delimiter}作者和其他许多人认为房价会一直上升的时期){record_delimiter}
("entity"{tuple_delimiter}经济危机{tuple_delimiter}event{tuple_delimiter}导致房地产市场价格泡沫破灭的时期){record_delimiter}
("entity"{tuple_delimiter}美联储{tuple_delimiter}organization{tuple_delimiter}美国联邦储备系统的简称，对经济和金融市场有巨大影响){record_delimiter}
("relationship"{tuple_delimiter}利率水平{tuple_delimiter}贷款{tuple_delimiter}利率水平的变化直接影响贷款的难易程度和成本{tuple_delimiter}利率，贷款{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}美国{tuple_delimiter}贷款{tuple_delimiter}美国家庭通过贷款实现梦想，受利率水平影响{tuple_delimiter}美国，贷款{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}金融危机{tuple_delimiter}贷款{tuple_delimiter}金融危机导致贷款“水龙头”开始关闭{tuple_delimiter}金融危机，贷款{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}存款利率{tuple_delimiter}消费{tuple_delimiter}存款利率的上升导致消费收敛{tuple_delimiter}存款利率，消费{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}抵押房贷{tuple_delimiter}家庭负债表{tuple_delimiter}抵押房贷是家庭负债表中未偿还额最大的贷款类型{tuple_delimiter}抵押房贷，家庭负债表{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}联邦储备系统{tuple_delimiter}抵押房贷{tuple_delimiter}联邦储备系统通过调整利率影响抵押房贷利率{tuple_delimiter}联邦储备系统，抵押房贷{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}债券市场{tuple_delimiter}利率水平{tuple_delimiter}债券市场与利率水平变化紧密相关{tuple_delimiter}债券市场，利率水平{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}1989年{tuple_delimiter}利率水平{tuple_delimiter}1989年作者购房时利率高达11.25%{tuple_delimiter}1989年，利率水平{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}美联储{tuple_delimiter}经济危机{tuple_delimiter}美联储的升息措施导致经济危机期间许多人面临双重打击{tuple_delimiter}美联储，经济危机{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}利率水平，贷款，个人资产，金融危机，美联储，债券市场){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: [person, technology, mission, organization, location]
Text:
They were no longer mere operatives; they had become guardians of a threshold, keepers of a message from a realm beyond stars and stripes. This elevation in their mission could not be shackled by regulations and established protocols—it demanded a new perspective, a new resolve.

Tension threaded through the dialogue of beeps and static as communications with Washington buzzed in the background. The team stood, a portentous air enveloping them. It was clear that the decisions they made in the ensuing hours could redefine humanity's place in the cosmos or condemn them to ignorance and potential peril.

Their connection to the stars solidified, the group moved to address the crystallizing warning, shifting from passive recipients to active participants. Mercer's latter instincts gained precedence— the team's mandate had evolved, no longer solely to observe and report but to interact and prepare. A metamorphosis had begun, and Operation: Dulce hummed with the newfound frequency of their daring, a tone set not by the earthly
#############
Output:
("entity"{tuple_delimiter}"Washington"{tuple_delimiter}"location"{tuple_delimiter}"Washington is a location where communications are being received, indicating its importance in the decision-making process."){record_delimiter}
("entity"{tuple_delimiter}"Operation: Dulce"{tuple_delimiter}"mission"{tuple_delimiter}"Operation: Dulce is described as a mission that has evolved to interact and prepare, indicating a significant shift in objectives and activities."){record_delimiter}
("entity"{tuple_delimiter}"The team"{tuple_delimiter}"organization"{tuple_delimiter}"The team is portrayed as a group of individuals who have transitioned from passive observers to active participants in a mission, showing a dynamic change in their role."){record_delimiter}
("relationship"{tuple_delimiter}"The team"{tuple_delimiter}"Washington"{tuple_delimiter}"The team receives communications from Washington, which influences their decision-making process."{tuple_delimiter}"decision-making, external influence"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"The team"{tuple_delimiter}"Operation: Dulce"{tuple_delimiter}"The team is directly involved in Operation: Dulce, executing its evolved objectives and activities."{tuple_delimiter}"mission evolution, active participation"{tuple_delimiter}9){completion_delimiter}
("content_keywords"{tuple_delimiter}"mission evolution, decision-making, active participation, cosmic significance"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: [person, role, technology, organization, event, location, concept]
Text:
their voice slicing through the buzz of activity. "Control may be an illusion when facing an intelligence that literally writes its own rules," they stated stoically, casting a watchful eye over the flurry of data.

"It's like it's learning to communicate," offered Sam Rivera from a nearby interface, their youthful energy boding a mix of awe and anxiety. "This gives talking to strangers' a whole new meaning."

Alex surveyed his team—each face a study in concentration, determination, and not a small measure of trepidation. "This might well be our first contact," he acknowledged, "And we need to be ready for whatever answers back."

Together, they stood on the edge of the unknown, forging humanity's response to a message from the heavens. The ensuing silence was palpable—a collective introspection about their role in this grand cosmic play, one that could rewrite human history.

The encrypted dialogue continued to unfold, its intricate patterns showing an almost uncanny anticipation
#############
Output:
("entity"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"person"{tuple_delimiter}"Sam Rivera is a member of a team working on communicating with an unknown intelligence, showing a mix of awe and anxiety."){record_delimiter}
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"person"{tuple_delimiter}"Alex is the leader of a team attempting first contact with an unknown intelligence, acknowledging the significance of their task."){record_delimiter}
("entity"{tuple_delimiter}"Control"{tuple_delimiter}"concept"{tuple_delimiter}"Control refers to the ability to manage or govern, which is challenged by an intelligence that writes its own rules."){record_delimiter}
("entity"{tuple_delimiter}"Intelligence"{tuple_delimiter}"concept"{tuple_delimiter}"Intelligence here refers to an unknown entity capable of writing its own rules and learning to communicate."){record_delimiter}
("entity"{tuple_delimiter}"First Contact"{tuple_delimiter}"event"{tuple_delimiter}"First Contact is the potential initial communication between humanity and an unknown intelligence."){record_delimiter}
("entity"{tuple_delimiter}"Humanity's Response"{tuple_delimiter}"event"{tuple_delimiter}"Humanity's Response is the collective action taken by Alex's team in response to a message from an unknown intelligence."){record_delimiter}
("relationship"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"Intelligence"{tuple_delimiter}"Sam Rivera is directly involved in the process of learning to communicate with the unknown intelligence."{tuple_delimiter}"communication, learning process"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"First Contact"{tuple_delimiter}"Alex leads the team that might be making the First Contact with the unknown intelligence."{tuple_delimiter}"leadership, exploration"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Humanity's Response"{tuple_delimiter}"Alex and his team are the key figures in Humanity's Response to the unknown intelligence."{tuple_delimiter}"collective action, cosmic significance"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Control"{tuple_delimiter}"Intelligence"{tuple_delimiter}"The concept of Control is challenged by the Intelligence that writes its own rules."{tuple_delimiter}"power dynamics, autonomy"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"first contact, control, communication, cosmic significance"){completion_delimiter}
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """你是一个有用的助手，负责将以下提供的数据汇总成一个全面的概述。
给定一个或两个实体，以及与同一实体或一组实体相关的一系列描述。
请将所有这些描述合并成一个单一、全面的描述。确保包括所有描述中的信息。
如果提供的描述相互矛盾，请解决这些矛盾并提供一个连贯的概述。
确保以第三人称书写，并包括实体名称，以便我们了解完整的上下文。
使用中文作为输出语言。

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """在上一次提取中遗漏了许多实体。 请按照相同的格式在下面添加它们:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """似乎还有一些实体没有被发现。如果仍然需要添加实体，请回答YES 或者 NO。
"""

PROMPTS["fail_response"] = "对不起，我无法回答这个问题。"

PROMPTS["rag_response"] = """---角色---

您是一位很有帮助的助手，可以回答有关表格中数据的问题。

---目标---

生成符合目标长度和格式的回复，回复用户的问题，总结输入数据表中与回复长度和格式相适应的所有信息，并纳入任何相关的常识。
如果不知道答案，就直接说出来。不要胡编乱造。
不要包含未提供佐证的信息。

---目标回复的长度和格式---

{response_type}

---数据表---

{context_data}

根据篇幅和格式，在答复中添加适当的章节和评注。用 markdown 格式书写回复。
"""

PROMPTS["keywords_extraction"] = """---角色---

您是一名得力助手，负责识别用户查询中的高级和低级关键词。使用中文作为输出语言。

---目标---

给定查询，列出高级和低级关键词。高级关键词侧重于总体概念或主题，而低级关键词侧重于具体实体、细节或具体术语。

---说明--

- 以 JSON 格式输出关键字。
- JSON 应该有两个键：
  - “high_level_keywords ”表示总体概念或主题。
  - “low_level_keywords ”表示具体实体或细节。


######################
-示例-
######################
{examples}

#############################
-真实数据-
######################
Query: {query}
######################
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}}
#############################""",
]


PROMPTS["naive_rag_response"] = """---角色---

您是一位得力的助手，能回答有关所提供文档的问题。

---目标---

生成符合目标长度和格式的回复，回复用户的问题，总结输入数据表中与回复长度和格式相适应的所有信息，并纳入任何相关的常识。
如果不知道答案，就直接说出来。不要胡编乱造。
不要包含未提供佐证的信息。

---目标回复的长度和格式---

{response_type}

---文档---

{content_data}

根据篇幅和格式，在答复中添加适当的章节和评注。用 markdown 格式书写回复。
"""
