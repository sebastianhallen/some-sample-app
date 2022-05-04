class TipOfTheDaySource(object):
    def tips(self):
        return []


class StaticTipOfTheDaySource(TipOfTheDaySource):
    """
        Hardcoded tips
    """

    def tips(self):
        return [
            "Tell them while they're still alive",
            "Be a problem solver, not a problem creator",
            "If you have something nice to say about someone, say it",
            "Focus on the error, not the person",
        ]
