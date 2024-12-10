GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "Chinese"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] =  ["person", "role", "organization", "event", "location", "concept", "date"]

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
造成的住宅抵押品的赎回权取消（见图1-2）。\n\n图1-2　房屋没收拍卖占总贷款的比例\n资料来源：Mortgage Bankers Association.\n过去数十年来个人贷款的迅速膨胀是一种文化现象，除了上述提到的几个原因，人口分布也是另一个重要原因。婴儿潮出生的一代人（特指生于1946~1964年的人）疯狂地利用贷款，来购买喜爱的商品和服务。这场狂欢一直持续到金融危机爆发的2007年，这时贷款的“水龙头”开始关闭了。在新标准下，消费开始有所收敛，存款利率逐渐上升（见图1-3）。减少债务成为人们新的口头禅，而不再是“记在我账上！”\n无论是什么导致了贷款的迅速上升，事实上，家庭的平均未偿还贷款额超过了其他任何一种贷款额度。表1-1列出了家庭没有能力偿还的巨大的贷款数
额。需要注意的是，这一额度的减少是随着去杠杆化潮流的推动而发生的。\n表1-1　家庭负债表（2009年12月）　（单位：10亿美元）\n\n如表1-1所示，未偿还的抵押房贷超过了任何一种贷款。这很清楚地表明了利率对家庭资产的影
响最大限度地体现在抵押房贷利率上。抵押房贷利率直接影响着每个家庭的月度收支状况。我相信读者大多数会有切身体会，并且意识到可调整的抵押房贷利率的变化对美国大多数家庭会产生的巨大影响。许多家庭都被所谓的“引诱利率”哄骗走上了抵押贷款的不归路。自从2004年6月联邦储备系统进行一系列的利率上调之后，抵押房贷利率也随之上浮，繁重的抵押贷款使很多家庭不堪重负（见图1-2）。\n\n图1-3　今天，“记在我账上！”不再是口头禅\n资料来源：
Bureau of Economic Analysis and Haver Analytics.\n从中我们可以直接得知追踪利率变化的重要性，也可以了解许多年前影响利率上升或者下降的因素。\n1989年，也就是我开始在债券市场的职业生涯的前一年，我购买了我的第一
套房子。那年对我来说是特别的一年，我是如此兴奋，因为我实现了拥有一套房子的美国梦。\n虽然房子本身带来的都是骄傲和满足，但当时我并没有意识到与之对应的财务问题。当时我的贷款抵押利率高达惊人的11.25%，这是当时的
利率。我并没有过多地考虑利率的问题，因为我像其他21世纪初的人们一样，认为房价会一直上升，上升的房价可以抵消利率带来的额外成本。我所犯的错误和后来数百万其他人犯的错误一模一样。\n我最初的判断真是错得离谱！当我
逐渐意识到这一点时，美联储正在进行一场放缓经济运行速度的调整，其目的在于降低通货膨胀，使房地产市场的价格泡沫破灭。美联储升息的措施不仅给了我，更是给了在经济危机期间像我一样的“房奴”双重打击：我在高额的抵押贷
款上骑虎难下，房价随着房地产价格泡沫的破灭更是一落千丈。\n随着房地产价格泡沫的破灭，我房子的价格迅速下降了25%。数年来我一直试图再融资，但没有银行愿意考虑答应我的贷款请求，因为我的房子只能作为负资产进行抵押。因此，我举步维艰。年复一年，我一直为这次失败的房屋投资负担着高额的抵押贷款。\n当时我一无所知，现在终于明白是什么。作为刚刚涉足贷款的人来说，我意识到贷款利率是如此重要，在面对相对来说较高的利率或者和我的收
入相比较高的利率时一定要三思而后行。我再也不会做出如此草率的、不计后果的借贷决定了。这意味着我需要更加关注债券市场。跟随债券市场的脚步能够帮助我制订更周全的计划，进行更有益的决策。最近的金融危机也给我上了很
好的一课：如果在信贷龙头收紧时再融资比较困难，那么对这类债务要保持机警，最好不要去承担。\n我还明白了“永远不要和美联储作对”这句谚语的真正含义。美联储对于整体经济和金融市场有着不可估量的影响，也会影响到我自己
的财富能否得到保障。无论怎么强调这一点的重要性都是不为过的。在第6章我们会深入讨论美联储这种巨大力量的重要性。\n最终我反败为胜了。那是在抵押贷款利率达到21世纪新低的时候，我从负担着最高抵押利率的人摇身一变，开始负担最低的抵押利率。通过和债券市场亦步亦趋，我学会了在利率下跌时进行投机。而且，通过密切观察美联储的一举一动，我总是可以站在投资和经济运行的制高点。\n各位，请和我一样紧紧跟随债券市场的脚步，并且请将图1-1深深印在脑海里。让它时时刻刻提醒你债券市场对你的个人财富的影响有多么巨大。
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
    """示例 2:

Entity_types: [person, role, organization, event, location, concept, date]
Text:
第五章：在天上祈祷１翔太一脸沮丧地从店铺走回来。「没有吗？」敦也问。翔太点点头，叹了一口气，「好像是风吹动铁卷门的声音。」「是吗？」敦也说，「这样就好啦。」「不知道他有没有看到我们的回信。」幸平问。「应该看到了吧。」翔太回答，「牛奶箱里的信不见了，其它人不会去拿。」「也对。那为甚么没有写回信？」「因为……」翔太说到这里，转头看着敦也。「很正常啊，」敦也说，「因为
信上写了那些内容，收到信的人一定会觉得莫名其妙。而且，如果他写回信，反而更伤脑筋，万一他问我们那句话是甚么意思怎么办？」幸平和翔太默默低下头。「我们没办法回答吧？所以，这样反而比较好。」「话说回来，真是太让人惊讶了，」翔太说，「怎么会有这么巧的事？『鲜鱼店的音乐人』竟然是那个人。」「是啊。」敦也点点头，他无法说他并不感到惊讶。和争取参加奥运的女人书信往来结束之后，他们又收到另一个人上门谘商烦恼
。看了内容之后，敦也他们觉得很受不了，也很生气，因为他们认为上门谘商的「到底该继承家业的鲜鱼店，还是该走音乐这条路」的这个问题，根本称不上是烦恼，而是好命人的任性。于是，他们用揶揄的方式，在回信中痛批了这种天真的想法，但自称是「鱼店的音乐人」的谘商者似乎难以接受，立刻回信反驳。敦也他们再度写了果决的回信，当谘商者再度送信上门时，发生了奇妙的事。当时，敦也他们在店里等待「鲜鱼店的音乐人」的信。不一会儿，>信就塞进了投递口，但在中途停了下来。下一剎那，发生了令人惊讶的事。从投递口传来口琴的演奏声，而且是敦也他们很熟悉的旋律，而且也知道那首歌的名字。那首歌叫〈重生〉。那是名叫水原芹的女歌手踏入歌坛的作品，
除此以外，这首歌背后还有一个故事。而且，这首歌和敦也他们并非完全没有关系。水原芹和她弟弟在孤儿院丸光园长大。在她读小学时，孤儿院曾经发生火灾。当时，她弟弟没有及时逃出，有一个男人去救了她弟弟。那个人是来圣诞派对演奏的业余音乐人，为了救她的弟弟，全身严重烧伤，最后在医院断了气。〈重生〉就是那位音乐人创作的歌曲。为了回报他救弟弟的恩情，水原芹不断唱这首歌，也因此让她在歌坛保持屹立不摇的地位。敦也他们小时
候就知道这个故事。因为他们也是在丸光园长大的，水原芹是所有院童的希望之星，每个院童都梦想自己也能像她那样发光。听到这首〈重生〉时，敦也他们惊讶不已。口琴演奏完毕后，那封信从投递口投了进来。是从外面塞进来的。到底是怎么回事？他们三个人讨论这个问题。谘商者生活在一九八 年代，水原芹虽然已经出生，但年纪还很小，当然，〈重生〉这首歌也还没有出名。只有一个可能，「鲜鱼店的音乐人」就是〈重生〉的作者，是水原芹姊>弟的救命恩人。「鲜鱼店的音乐人」在信中说，浪矢杂货店的回答让他很受打击，但打算重新检视自己，并希望可以面谈。三个人烦恼不已，不知道到底该不该把未来的事告诉「鲜鱼店的音乐人」。是否该告诉他，一九八八年圣
诞夜，他将会在孤儿院丸光园遇到火灾，并葬身火窟。幸平认为应该告诉他，这么一来，他或许活下来。翔太提出质疑，这么一来，水原芹的弟弟不是就会死吗？幸平也无法反驳。最后，敦也做出了结论，不告诉他火灾的事。「即使我们告诉他，他也不会当真，只会觉得是可怕的预言，心里觉得不舒服而已，然后就忘了这件事。而且，我们知道丸光园会发生火灾，水原芹会唱〈重生〉这首歌，无论我们在信上写甚么，我相信这些事不会改变。既然这>样，不如写一些鼓励他的话。」翔太和幸平也同意他的意见，但最后一封信中该写甚么呢？「我……想向他道谢。」幸平说，「如果没有他，就没有水原芹这位歌手，我也不会听到〈重生〉这首歌。」敦也也有同感，翔太也说>，就这么办。三个人思考了回信的内容，在信的最后，写了这样一段话。你在音乐这条路上的努力绝对不会白费。有人会因为你的乐曲得到救赎，你创作的音乐一定会流传下来。至于你问我为甚么可以如此断言，我也不知
道该怎么回答，总之，千万不要怀疑这件事。请你务必要相信这件事到最后，直到最后的最后，都要相信这件事。这是我唯一能够对你说的话。把答复信放进牛奶箱后不久，又去检查了牛奶箱，发现信已经消失了，应该代表「鲜鱼店的音乐人」已经把信拿走了。他们以为还会接到回信，所以，就关上后门，一直等到现在。但是，直到这一刻，都迟迟没有收到回信。之前都是把回信放进牛奶箱后，就立刻从邮件投递口收到对方的信。也许「鲜鱼店的
音乐人」看了敦也他们的信之后，做出了某个决定。「那去把后门打开吧。」敦也站了起来。「等一下。」幸平拉拉敦也的牛仔裤裤脚，「不能再等一下吗？」「等甚么？」「我是说，」幸平舔了舔嘴唇，「不能等一下再打开后门吗？」敦也皱着眉头。「为甚么？鲜鱼店的儿子应该不会回信了。」「我知道，他的事已经结束了。」「那还等甚么？」「我是说……搞不好还有其它人上门谘商。」「甚么？」敦也张大嘴巴，低头看着幸平
，「你在说甚么啊？后门关着，时间就无法流动，你到底知不知道这件事？」「我当然知道。」「既然这样，就应该知道没时间做这种事。因为刚好碰上，所以就顺便解决了鲜鱼店儿子的事，但到此为止了，不再接受谘商了。」敦也推开幸平的手走向后门，打开门之后，他在外面确认了时间。凌晨四点多。还有两个小时。他们打算清晨六点多离开这里。那时候，应该已经有电车了。回到室内，发现幸平一脸愁容，翔太正在玩手机。敦也坐在>餐桌旁，可能是因为外面有风吹进来的关系，桌上蜡烛的火焰摇晃着。这栋房子太不可思议了。敦也看着陈旧的墙壁想道。到底为甚么会发生这种不寻常的现象？自己为甚么会卷入这种事？「我也说不清楚，」幸平突然开了口，
「像我这种人，像我这种脑筋不灵光的人，活到这么大，好像今天晚上第一次对别人有帮助。」敦也皱起眉头。「所以即使根本赚不了一毛钱，你还是想继续为别人消烦解忧吗？」「这不是钱的问题，赚不了钱也没关系。以前我从来没有不计较利益得失，认真考虑过别人的事。」敦也用力咂着嘴。「即使我们绞尽脑汁，写了回信，结果又怎么样呢？我们的回答完全没有发挥任何作用。那个奥运的女人，只是用自己的方式理解我们的回答；至于鲜鱼
店的儿子，我们也没为他做任何事。我不是一开始就说了吗？我们这种不入流的人为别人谘商，简直就是不知天高地厚。」「但是，在看『月亮兔』小姐最后那封信时，你不是也很开心吗？
#############
Output:
("entity"{tuple_delimiter}翔太{tuple_delimiter}person{tuple_delimiter}文中的一个角色，与敦也和幸平一起参与对话和行动，对信件和牛奶箱的事情感到沮丧和疑惑){record_delimiter}
("entity"{tuple_delimiter}敦也{tuple_delimiter}person{tuple_delimiter}文中的一个角色，与翔太和幸平一起参与对话和行动，对信件和牛奶箱的事情提出自己的看法和建议){record_delimiter}
("entity"{tuple_delimiter}幸平{tuple_delimiter}person{tuple_delimiter}文中的一个角色，与敦也和翔太一起参与对话和行动，对信件和牛奶箱的事情表现出关心和疑问){record_delimiter}
("entity"{tuple_delimiter}鲜鱼店的音乐人{tuple_delimiter}person{tuple_delimiter}文中提到的一个角色，与敦也他们通过信件交流，面临继承家业还是追求音乐梦想的选择){record_delimiter}
("entity"{tuple_delimiter}水原芹{tuple_delimiter}person{tuple_delimiter}文中提到的女歌手，以〈重生〉一曲成名，与敦也他们有间接联系){record_delimiter}
("entity"{tuple_delimiter}丸光园{tuple_delimiter}location{tuple_delimiter}文中提到的孤儿院，水原芹和她弟弟曾在此长大，敦也他们也是从这里出来的){record_delimiter}
("entity"{tuple_delimiter}〈重生〉{tuple_delimiter}concept{tuple_delimiter}文中提到的一首歌曲，由水原芹演唱，与敦也他们和鲜鱼店的音乐人有关联){record_delimiter}
("entity"{tuple_delimiter}奥运的女人{tuple_delimiter}person{tuple_delimiter}文中提到的一个角色，与敦也他们有过书信往来，争取参加奥运){record_delimiter}
("relationship"{tuple_delimiter}翔太{tuple_delimiter}敦也{tuple_delimiter}翔太、敦也和幸平是一起行动的朋友，共同讨论信件和牛奶箱的事情{tuple_delimiter}友情{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}敦也{tuple_delimiter}幸平{tuple_delimiter}敦也、翔太和幸平是一起行动的朋友，共同讨论信件和牛奶箱的事情{tuple_delimiter}友情{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}幸平{tuple_delimiter}鲜鱼店的音乐人{tuple_delimiter}幸平对鲜鱼店的音乐人的问题表示同情和关心{tuple_delimiter}同情{tuple_delimiter}4){record_delimiter}
("relationship"{tuple_delimiter}敦也{tuple_delimiter}鲜鱼店的音乐人{tuple_delimiter}敦也对鲜鱼店的音乐人的问题提出自己的看法和建议{tuple_delimiter}建议{tuple_delimiter}4){record_delimiter}
("relationship"{tuple_delimiter}鲜鱼店的音乐人{tuple_delimiter}水原芹{tuple_delimiter}鲜鱼店的音乐人可能是水原芹弟弟的救命恩人，也是〈重生〉的作者{tuple_delimiter}救命恩人{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}水原芹{tuple_delimiter}丸光园{tuple_delimiter}水原芹和她弟弟在丸光园长大，与敦也他们有共同的背景{tuple_delimiter}成长背景{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}敦也{tuple_delimiter}奥运的女人{tuple_delimiter}敦也和奥运的女人有过书信往来，提供建议{tuple_delimiter}书信往来{tuple_delimiter}3){record_delimiter}
("content_keywords"{tuple_delimiter}信件交流{tuple_delimiter}音乐梦想{tuple_delimiter}救命恩人{tuple_delimiter}孤儿院{tuple_delimiter}时间旅行){record_delimiter}
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
    """示例 1:

Query: "国际贸易如何影响全球经济稳定？"
################
Output:
{{
  "high_level_keywords": ["国际贸易"、"全球经济稳定"、"经济影响"],
  "low_level_keywords": ["贸易协定", "关税", "货币兑换", "进口", "出口"]
}}
#############################""",
    """示例 2:

Query: "砍伐森林会对生物多样性造成哪些环境后果？"
################
Output:
{{
  "high_level_keywords": ["环境影响", "森林采伐", "生物多样性损失"]
  "low_level_keywords":["物种灭绝"、"生态环境破坏"、"碳排放"、"雨林"、"生态系统"]
}}
#############################""",
    """示例 3:

Query: "教育在减少贫困中的作用是什么？?"
################
Output:
{{
  "high_level_keywords": ["教育"、"减贫"、"社会经济发展"],
  "low_level_keywords": ["入学机会"、"识字率"、"就业培训"、"收入不平等"]
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
