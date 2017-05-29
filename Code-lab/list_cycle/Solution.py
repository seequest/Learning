""" [Facebook Code Lab: Listcycle](https://codelab.interviewbit.com/problems/listcycle/)

Given a linked list, return the node where the cycle begins. If there is no cycle, return null.

Try solving it using constant additional space.

Example:

Input: 
               ┌────┐
               │    │
               ↓    │
     1 -> 2 -> 3 -> 4

Return the node corresponding to node 3. 

Implementation notes
--------------------

The name of the function provided by Facebook Code Lab--detect_cycle--is a misleading. There are two parts to this 
solution:
 
1. Detecting that the list is cyclic and then--if the list is cyclic--
   
2. Finding the first node of the cycle.

We know that Floyd’s Cycle detection algorithm terminates when fast and slow references meet at a common node. There is
no guarantee that the common node is the first node in the cycle. Hence, we must look for it.

"""
from typing import Any, Sequence, Optional


class SinglyLinkedList:

    def __init__(self, values: Sequence[Any], cycle: Optional[int]):

        if not values:
            self.head = None
            return

        cycle_back = None
        previous = None

        for index, value in enumerate(values):
            node = SinglyLinkedList.Node(value, index)
            if previous is None:
                self.head = node
            else:
                previous.next = node
            if index == cycle:
                cycle_back = node
            previous = node

        previous.next = cycle_back

    def detect_cycle(self) -> Optional['SinglyLinkedList.Node']:
        """
        :return: first node in the cycle in the linked list or :const:`None`, if the list is acyclic.

        """
        return self._detect_cycle(self.head)

    @staticmethod
    def _detect_cycle(head: 'SinglyLinkedList.Node') -> Optional['SinglyLinkedList.Node']:

        # Detect a cycle in the list and--if there is one--find the start of the cycle using [Floyd's cycle detection
        # algorithm](https://goo.gl/6CkCS7) (a.k.a., The tortoise and the hare algorithm for cycle detection)

        if head is None or head.next is None:
            return head

        tortoise = head.next
        hare = tortoise.next

        while tortoise is not hare:
            if None in (hare, hare.next):
                return None
            tortoise = tortoise.next
            hare = hare.next.next

        # If we retrace tortoise's steps while advancing hare within the cycle at the same rate, they will meet at the
        # start of the cycle. The mathematics behind this is straight forward:
        #
        #   Let T be the number of nodes before the beginning of the cycle.
        #   Let C be the number of noes in the cycle.
        #
        #   Hence, for example, T = 2, C = 2 in this cyclic list:
        #
        #                ┌────┐
        #                │    │
        #                ↓    │
        #      1 -> 2 -> 3 -> 4
        #
        # We call the nodes in the range of T the tail nodes. We call the nodes in the range of C the cycle nodes. After
        # T steps, tortoise is at the first node of the cycle (node 3) and hare is at T + r, where r = T (mod C), the
        # same position (node 3)
        #
        # More generally that after T steps by tortoise, hare is this position in the cycle:
        #
        #   T = λC + r, 0 <= r < C
        #
        # After T steps, tortoise is at node r = 0 and hare is at node r, where r = T - λC. Hence, after another C - r
        # steps tortoise is at node C - r and hare is at a congruent location:
        #
        #   r + 2(C - r) (mod C) =
        #   r + 2C - 2r (mod C) =
        #   2C - r (mod C) =
        #   C - r
        #
        # Hence, the distance from the start when tortoise meets hare is
        #
        #   T + C - r =
        #   (λC + r) + C - r =
        #   (λ + 1)C
        #
        # which is a multiple of the cycle length, C.
        #
        # When we move the tortoise back to the start and move both tortoise and hare forward T steps,
        #
        #   tortoise is at the start of the cycle
        #
        # while hare has moved from
        #
        #   C − r
        #
        # to
        #
        #   (C - r) + T =
        #   (C - r) + (λC + r) =
        #   (λ + 1)C
        #
        # And given that
        #
        #   (λ + 1)C (mod C) = 0
        #
        # we see that tortoise and hare are at the start of the cycle at the same time.

        tortoise = head

        while tortoise is not hare:
            tortoise = tortoise.next
            hare = hare.next

        return tortoise

    class Node:

        def __init__(self, value: Any, index: int):
            self.value = value
            self.index = index
            self.next = None

        def __str__(self):
            return f'[{self.index}]={self.value}'


def test(sequence: Sequence[Any], cycle_back: Optional[int]):

    print()
    print('length:', len(sequence), 'sequence:', sequence)
    print('expected: index =', -1 if cycle_back is None else cycle_back)

    singly_linked_list = SinglyLinkedList(sequence, cycle_back)
    result = singly_linked_list.detect_cycle()

    print('observed: index =', -1 if result is None else result.index)

test([1], cycle_back=0)
test([1, 2, 3, 4], cycle_back=2)
test([87797, 23219, 41441, 58396, 48953, 94603, 2721, 95832, 49029, 98448, 65450], cycle_back=None)
test([
    82190, 96115, 22444, 88260, 23907, 89813, 64104, 52843, 86614, 47123, 87579, 47274, 68834, 64297, 69892, 81076,
    9595, 16501, 41237, 26173, 75029, 82215, 19042, 89320, 34501, 23104, 56160, 62828, 83488, 52016, 87137, 62728, 2149,
    16312, 99398, 34159, 57564, 72572, 76732, 7942, 39260, 66779, 17414, 28032, 63991, 90726, 85268, 57484, 29209,
    87322, 34383, 86070, 93870, 41624, 35470, 89832, 10435, 10030, 39777, 43247, 17688, 99890, 41871, 9641, 64437,
    16706, 2609, 20826, 67212, 97997, 17514, 65885, 92345, 80918, 36462, 85164, 96232, 80800, 99258, 96801, 76016,
    30844, 72748, 89080, 98273, 50246, 52852, 92790, 19880, 64796, 68000, 2618, 10437, 6474, 9204, 71181, 33164, 6692,
    37780, 94836, 9765, 58958, 79589, 96391, 62639, 34125, 55248, 48511, 61202, 77093, 91268, 22076, 54825, 37483,
    96237, 12024, 84617, 33450, 46720, 72392, 91671, 65512, 34772, 57372, 24399, 38609, 47117, 56144, 26795, 49, 23925,
    90457, 93835, 9951, 62395, 48935, 61838, 4574, 64350, 88408, 47817, 72220, 54891, 99168, 23620, 4102, 74540, 96744,
    8291, 11307, 78192, 57146, 98345, 84366, 49512, 14740, 3787, 77779, 70044, 92426, 66274, 99948, 6139, 59654, 58456,
    19983, 37467, 29222, 13445, 44903, 31287, 83838, 22331, 14004, 54830, 12743, 21781, 46554, 48185, 27257, 42980,
    9671, 27493, 14412, 71825, 71285, 33488, 41172, 75380, 12600, 19569, 98928, 26887, 540, 4611, 82938, 84231, 77253,
    31506, 28609, 73503, 18203, 82093, 31202, 42242, 95113, 88731, 86400, 55155, 87149, 69273, 38679, 39094, 96826,
    8491, 6548, 47037, 30435, 53744, 29090, 66245, 28617, 14536, 81340, 82778, 88353, 46062, 57727, 60949, 97250, 47252,
    78120, 68764, 83204, 53146, 22614, 7729, 76703, 74632, 60438, 97004, 7519, 58841, 4141, 55345, 34426, 23469, 44319,
    95489, 89247, 43571, 32771, 52036, 81965, 1012, 36753, 62746, 39371, 94219, 26772, 31515, 88035, 53713, 42103,
    42841, 44606, 76836, 27944, 10526, 13866, 80963, 55283, 53259, 86289, 64081, 8825, 37340, 85504, 38261, 15080,
    51485, 77133, 85420, 82363, 82008, 31818, 23792, 79923, 27683, 70891, 48804, 62453, 51128, 74294, 77182, 86910,
    4965, 76537, 33390, 30337, 21660, 46337, 52888, 81824, 90133, 22011, 65730, 18303, 42268, 29120, 48733, 1535, 35747,
    63895, 38610, 11189, 59655, 56220, 75166, 60612, 86557, 27584, 98539, 84315, 19973, 77033, 50442, 67707, 87931,
    33807, 21175, 42057, 27557, 46678, 33554, 52493, 75461, 50894, 41533, 50162, 32997, 48351, 5654, 73498, 5391, 90566,
    59412, 35476, 65492, 68312, 15328, 81977, 51070, 14763, 81858, 39691, 21699, 16881, 6163, 27641, 59355, 75637,
    88078, 55789, 79180, 6964, 53767, 87367, 22938, 32791, 83892, 85780, 4861, 22682, 23772, 30590, 36522, 23473, 76424,
    41046, 86232, 26749, 76625, 75663, 15781, 74065, 13993, 81926, 66460, 32658, 47980, 34849, 90271, 26560, 24849,
    10684, 43293, 6836, 26575, 80044, 31772, 24984, 50110, 45840, 67457, 47075, 75120, 20223, 66848, 97753, 63410, 943,
    81850, 38187, 63299, 73737, 82219, 79889, 53039, 13200, 1691, 91596, 90470, 21451, 39135, 88399, 50370, 86591,
    55132, 2982, 86558, 3241, 30107, 45759, 42830, 1264, 33723, 39549, 47675, 34762, 76463, 60107, 91748, 78494, 56237,
    2012, 79950, 27991, 63300, 24555, 70046, 18386, 3966, 72981, 21495, 44867, 47310, 98221, 22143, 91420, 87043, 86218,
    81860, 19866, 82255, 29778, 37889, 83667, 91524, 62023, 63998, 35412, 85376, 41004, 31102, 18703, 11479, 70536,
    36362, 87857, 43170, 64984, 18695, 45980, 91195, 19419, 11904, 98347, 65634, 74427, 35632, 98680, 56942, 48376,
    8887, 92332, 72826, 51333, 36994, 5971, 96829, 41774, 38674, 70854, 6774, 98577, 82262, 54743, 24748, 91532, 52427,
    90834, 17881, 84198, 15498, 16075, 19006, 27558, 67322, 77841, 467, 52349, 66591, 1773, 7548, 4432, 64605, 46290,
    37662, 22917, 66905, 34684, 72264, 90658, 5895, 14883, 65384, 50258, 2152, 76974, 76733, 80335, 94622, 7067, 27323,
    93654, 63508, 47140, 43910, 72602, 86026, 40599, 22412, 36469, 69884, 32018, 1249, 53992, 93293, 70356, 7627, 33620,
    50706, 96961, 54371, 85772, 48202, 37746, 66099, 81634, 51450, 646, 61868, 75216, 81707, 926, 59684, 18168, 33478,
    22962, 57215, 89252, 2590, 52615, 2188, 84678, 79583, 23175, 72245, 65583, 71690, 85160, 86838, 36238, 61900, 67926,
    91129, 58073, 69255, 56116, 5166, 79279, 32382, 28091, 24826, 92891, 5298, 3930, 88670, 94318, 65433, 29726, 68671,
    59321, 87800, 67921, 40693, 86625, 22163, 8521, 9873, 26483, 13641, 68206, 62224, 76112, 92251, 34990, 93361, 43902,
    36272, 65852, 11585, 54995, 46465, 50595, 74166, 38221, 19577, 11789, 53869, 42308, 55901, 19202, 52781, 81643,
    6150, 8973, 35752, 18480, 29700, 44418, 6536, 54490, 90173, 96843, 45105, 25466, 43652, 19177, 27133, 77447, 95447,
    7557, 21007, 46823, 89816, 50152, 3291, 51156, 71211, 20174, 88350, 34840, 76652, 27724, 22846, 44281, 96711, 61319,
    96385, 62832, 20950, 95690, 28913, 85775, 94278, 60051, 66820, 92061, 77079, 67289, 94892, 93304, 41447, 5299,
    31729, 82678, 9908, 78843, 5723, 92589, 5884, 50500, 61591, 93021, 58826, 11209, 99986, 13608, 56145, 52893, 47108,
    96803, 6755, 60282, 76805, 9221, 68642, 94698, 90076, 30479, 37308, 2177, 62130, 90250, 46934, 92794, 17439, 45594,
    77122, 32987, 40097, 6250, 93826, 67016, 23592, 21983, 12711, 74089, 41761, 64135, 34311, 72533, 95527, 32308
], cycle_back=191)
