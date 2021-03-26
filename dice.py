from lark import Lark, Transformer, v_args
import random

DIE_GRAMMAR = r"""
   ?start: arithmetic

   ?arithmetic: value (math_op)*

   ?math_op: (plus|minus) value

   ?minus: "-"
   ?plus: "+"

   ?value: dice | number
   ?dice: INT "d" INT
   ?number: INT -> number

   %import common.SIGNED_INT
   %import common.INT
"""

class InterpretDiestring(Transformer):

    @v_args(inline=True)
    def number(self, num):
        num = int(num)
        return (str(num), num)
            
    @v_args(inline=True)
    def dice(self, count, sides):
        count = int(count)
        sides = int(sides)
        rolls = [random.randint(1, sides) for d in range(count)]
        return (
            "[{}d{}: {}]".format(count, sides, ", ".join(str(r) for r in rolls)),
            sum(rolls)
        )
        
        
    def arithmetic(self, elements):
        return (
            "".join(
                e[0]
                for e in elements
            ),
            sum(
                e[1]
                for e in elements
            )
        )


    @v_args(inline=True)
    def math_op(self, op, expr):
        op_str, mult = op
        expr_str, expr_value = expr
        return (
            " {} {}".format(op_str, expr_str),
            mult * expr_value
        )
        
    def minus(self, v):
        return ("-", -1)
    def plus(self, v):
        return ("+", 1)

# Based on example here:
# https://github.com/lark-parser/lark/blob/master/examples/json_parser.py
PARSER = Lark(
    DIE_GRAMMAR,
    parser="lalr",
    lexer = 'standard',
    propagate_positions=False,
#    maybe_placeholders=False,
    transformer=InterpretDiestring()
)
roll = PARSER.parse

#if __name__ == "__main__":
#    print(roll("1d6+23-5d6"))
