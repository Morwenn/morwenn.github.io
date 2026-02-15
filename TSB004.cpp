#include <algorithm>
#include <cassert>
#include <forward_list>
#include <functional>
#include <iomanip>
#include <iostream>
#include <iterator>
#include <ranges>
#include <tuple>
#include <utility>
#include <vector>

template<std::size_t Index, std::size_t... Indices>
struct make_reversed_index_sequence:
    make_reversed_index_sequence<Index - 1, Indices..., Index - 1>
{};

template<std::size_t... Indices>
struct make_reversed_index_sequence<0, Indices...>:
    std::index_sequence<Indices...>
{};


namespace std
{
template<typename F>
struct flip_t
{
    private:
        F func;

        template<typename Self, typename Tuple, std::size_t... Indices>
        static auto _call(Self&& self, Tuple&& args, std::index_sequence<Indices...>)
            -> decltype(std::invoke(
                std::forward<Self>(self).func,
                std::get<Indices>(std::forward<Tuple>(args))...
            ))
        {
            return std::invoke(
                std::forward<Self>(self).func,
                std::get<Indices>(std::forward<Tuple>(args))...
            );
        }

        template<typename Self, typename Tuple>
        static auto _call(Self&& self, Tuple&& args)
            -> decltype(_call(
                std::forward<Self>(self),
                std::forward<Tuple>(args),
                make_reversed_index_sequence<std::tuple_size_v<Tuple>>{}
            ))
        {
            return _call(
                std::forward<Self>(self),
                std::forward<Tuple>(args),
                make_reversed_index_sequence<std::tuple_size_v<Tuple>>{}
            );
        }

    public:
        // Construction

        flip_t() = default;

        explicit constexpr flip_t(F&& func):
            func(std::move(func))
        {}

        // Call

        template<typename... Args>
        constexpr auto operator()(Args&&... args) &
            -> decltype(_call(*this, std::forward_as_tuple(std::forward<Args>(args)...)))
        {
            return _call(*this, std::forward_as_tuple(std::forward<Args>(args)...));
        }

        template<typename... Args>
        constexpr auto operator()(Args&&... args) const&
            -> decltype(_call(*this, std::forward_as_tuple(std::forward<Args>(args)...)))
        {
            return _call(*this, std::forward_as_tuple(std::forward<Args>(args)...));
        }

        template<typename... Args>
        constexpr auto operator()(Args&&... args) &&
            -> decltype(_call(*this, std::forward_as_tuple(std::forward<Args>(args)...)))
        {
            return _call(*this, std::forward_as_tuple(std::forward<Args>(args)...));
        }

        template<typename... Args>
        constexpr auto operator()(Args&&... args) const&&
            -> decltype(_call(*this, std::forward_as_tuple(std::forward<Args>(args)...)))
        {
            return _call(*this, std::forward_as_tuple(std::forward<Args>(args)...));
        }

        // Accessor

        [[nodiscard]]
        constexpr auto base() const
            -> F
        {
            return func;
        }
};

// flip

template<typename F>
constexpr auto flip(F func)
    -> flip_t<F>
{
    return flip_t<F>(std::move(func));
}

template<typename F>
constexpr auto flip(flip_t<F> flipped_func)
    -> F
{
    return flipped_func.base();
}
}


template<typename Iterator, typename Compare>
bool is_reverse_sorted(Iterator begin, Iterator end, Compare compare)
{
    return std::is_sorted(begin, end, std::flip(compare));
}

template<typename Iterator, typename T, typename Compare>
auto my_upper_bound(Iterator begin, Iterator end, T const& value, Compare compare)
    -> Iterator
{
    return std::lower_bound(
        begin, end, value,
        std::not_fn(std::flip(compare))
    );
}





namespace boost::algorithm
{
// TODO: doc
struct iterator_output_tag {
};
// TODO: doc
struct value_output_tag {
};

/// Longest increasing subsequence algorithm.
///
/// @time O(N logN)
/// @space O(N)
template < typename RandomIterator,
           typename Comparator = std::less<
               typename std::iterator_traits< RandomIterator >::value_type > >
class longest_increasing_subsequence {
    typedef typename std::iterator_traits< RandomIterator >::difference_type
        difference_type;
    typedef
        typename std::iterator_traits< RandomIterator >::value_type value_type;

public:
    typedef std::vector< RandomIterator > iterator_vector;
    typedef std::vector< value_type > value_vector;

    longest_increasing_subsequence ( Comparator cmp = Comparator () )
        : compare ( cmp )
    {
    }

    ~longest_increasing_subsequence () {}

    /// \brief Searches the longest (increasing) subsequence in the sequence
    ///
    /// The result is a vector of iterators defining the longest increasing
    /// subsequence (possibly non-continuous elements). By giving a different
    /// comparison predicate to the constructor, one can find as well, e.g., the
    /// longest decreasing subsequence (with std::greater<T>() predicate) or the
    /// non-decreasing one (with std::not1(std::greater<T>())).
    /// The time complexity of the algorithm is log-linear O(n logn) where n is
    /// the length of the sequence (`std::distance(first, last)`).
    /// The space complexity is linear O(n).
    ///
    /// \param first        The start of the sequence to search (Random Access
    /// Iterator)
    /// \param last         One past the end of the sequence to search
    ///
    value_vector operator()( RandomIterator first, RandomIterator last,
                             value_output_tag tag ) const
    {
        return this->do_search_and_output ( first, last, tag );
    }

    iterator_vector operator()( RandomIterator first, RandomIterator last,
                                iterator_output_tag tag ) const
    {
        return this->do_search_and_output ( first, last, tag );
    }

    template < typename OutputIterator >
    OutputIterator operator()( RandomIterator first, RandomIterator last,
                               OutputIterator d_first ) const
    {
        return this->do_search_and_output ( first, last, d_first );
    }

private:
    /// \cond DOXYGEN_HIDE
    Comparator compare;

    typedef std::size_t size_type;
    typedef std::vector< size_type > index_vector;

    size_type
    do_search ( RandomIterator first, RandomIterator last ) const
    {
        index_vector predecessor;
        index_vector lis_tail;
        return do_search ( first, last, predecessor, lis_tail );
    }

    size_type
    do_search ( RandomIterator first, RandomIterator last,
                /*output*/ index_vector &predecessor,
                /*output*/ index_vector &lis_tail ) const
    {
        difference_type const n = std::distance ( first, last );
        /// Length of the longest (increasing) subsequence found so far
        size_type lis_length = 0;
        /// predecessor[k, 0 <= k < n] - stores the index of the predecessor of
        /// X[k] in the longest increasing subsequence ending at X[k]
        predecessor.resize ( n );
        /// lis_tail[j, 0 <= k <= n] - stores the index k of the smallest value
        /// X[k] such that there is an increasing subsequence of length j ending
        /// at X[k] on the range k <= i (note we have j <= k <= i here, because
        /// j represents the length of the increasing subsequence, and k
        /// represents the index of its termination.
        /// Obviously, we can never have an increasing subsequence of length 13
        /// ending at index 11. k <= i by definition).
        lis_tail.resize ( n + 1 );

        for ( difference_type i = 0; i < n; ++i ) {
            // Binary search for the largest positive j <= lis_length, such that
            // X[lis_tail[j]] < X[i].
            // After searching, lo is 1 greater than the length of the longest
            // prefix of X[i].
            size_type new_lis_length;
            {
                size_type lo = 1;
                size_type hi = lis_length;
                while ( lo <= hi ) {
                    size_type mid = ( lo + hi ) / 2;
                    assert ( mid <= i );
                    if ( compare (
                             *( first + lis_tail[mid] ),
                             *( first + i ) ) ) {  // X[lis_tail[mid]] < X[i]
                        lo = mid + 1;
                    }
                    else {
                        hi = mid - 1;
                    }
                }
                new_lis_length = lo;
            }

            // The predecessor of X[i] is the last index of the subsequence of
            // length new_lis_length-1
            assert ( new_lis_length > 0 );
            predecessor[i] = lis_tail[new_lis_length - 1];

            assert ( new_lis_length <= n );
            assert ( lis_tail[new_lis_length] < n );
            if ( new_lis_length > lis_length ) {
                // If we found a subsequence longer than any we have found yet,
                // update lis_tail and lis_length
                lis_tail[new_lis_length] = i;
                lis_length = new_lis_length;
            }
            else if ( compare ( *( first + i ),
                                *( first + lis_tail[new_lis_length] ) ) ) {
                // X[i] < X[lis_tail[new_lis_length]]
                // If we found a smaller last value for the subsequence of
                // length new_lis_length, only update lis_tail
                lis_tail[new_lis_length] = i;
            }
        }
        return lis_length;
    }

    template < typename OutputIterator >
    OutputIterator
    do_output ( RandomIterator first, RandomIterator /*last*/,
                size_type lis_length, index_vector const &predecessor,
                index_vector const &lis_tail, OutputIterator d_first ) const
    {
        // Reconstruct the longest increasing subsequence
        index_vector lis ( lis_length );
        size_type k = lis_tail[lis_length];
        for ( size_type i = lis_length; i--; ) {
            lis[i] = k;  // X[k];
            k = predecessor[k];
        }
        // Output the found subsequence
        for ( size_type i = 0; i < lis_length; ++i ) {
            *d_first++ = *( first + lis[i] );
        }
        return d_first;
    }

    value_vector
    do_output ( RandomIterator first, RandomIterator /*last*/,
                size_type lis_length, index_vector const &predecessor,
                index_vector const &lis_tail, value_output_tag /*tag*/ ) const
    {
        // Reconstruct the longest increasing subsequence values
        value_vector lis ( lis_length );
        size_type k = lis_tail[lis_length];
        for ( size_type i = lis_length; i--; ) {
            lis[i] = *( first + k );  // X[k];
            k = predecessor[k];
        }
        return lis;
    }

    iterator_vector
    do_output ( RandomIterator first, RandomIterator /*last*/,
                size_type lis_length, index_vector const &predecessor,
                index_vector const &lis_tail,
                iterator_output_tag /*tag*/ ) const
    {
        // Reconstruct the longest increasing subsequence iterators
        iterator_vector lis ( lis_length );
        size_type k = lis_tail[lis_length];
        for ( size_type i = lis_length; i--; ) {
            lis[i] = first + k;  // &X[k];
            k = predecessor[k];
        }
        return lis;
    }

    template < typename OutputIterator >
    OutputIterator
    do_search_and_output ( RandomIterator first, RandomIterator last,
                           OutputIterator d_first ) const
    {
        index_vector predecessor;
        index_vector lis_tail;
        size_type lis_length = do_search ( first, last, predecessor, lis_tail );
        return do_output ( first, last, lis_length, predecessor, lis_tail,
                           d_first );
    }

    value_vector
    do_search_and_output ( RandomIterator first, RandomIterator last,
                           value_output_tag tag ) const
    {
        index_vector predecessor;
        index_vector lis_tail;
        size_type lis_length = do_search ( first, last, predecessor, lis_tail );
        return this->do_output ( first, last, lis_length, predecessor, lis_tail,
                                 tag );
    }

    iterator_vector
    do_search_and_output ( RandomIterator first, RandomIterator last,
                           iterator_output_tag tag ) const
    {
        index_vector predecessor;
        index_vector lis_tail;
        size_type lis_length = do_search ( first, last, predecessor, lis_tail );
        return this->do_output ( first, last, lis_length, predecessor, lis_tail,
                                 tag );
    }
    // \endcond
};

}


template<typename Iterator, typename Compare>
auto longest_increasing_subsequence(Iterator begin, Iterator end, Compare compare)
{
    boost::algorithm::longest_increasing_subsequence<Iterator, Compare> lis(compare);
    return lis(begin, end, boost::algorithm::value_output_tag{});
}

template<typename Iterator, typename Compare>
auto longest_decreasing_subsequence(Iterator begin, Iterator end, Compare compare)
{
    return longest_increasing_subsequence(begin, end, std::flip(compare));
}

template<typename Iterator, typename Compare>
auto longest_non_decreasing_subsequence(Iterator begin, Iterator end, Compare compare)
{
    return longest_increasing_subsequence(begin, end, std::not_fn(std::flip(compare)));
}

template<typename Iterator, typename Compare>
auto longest_non_increasing_subsequence(Iterator begin, Iterator end, Compare compare)
{
    return longest_increasing_subsequence(begin, end, std::not_fn(compare));
}

template<typename Range, typename T, typename Func>
auto do_fold_right(Range&& range, T init, Func func)
{
    return std::ranges::fold_left(
        std::forward<Range>(range) | std::views::reverse,
        std::move(init),
        std::flip(func)
    );
}


int main()
{
    std::cout << std::boolalpha;

    // is_reverse_sorted
    {
        std::vector<int> vec = {10, 9, 8, 8, 8, 7, 6, 5, 5, 4, 3, 2, 1, 0, 0, 0};
        std::cout << "Sorted? " << std::is_sorted(vec.begin(), vec.end(), std::less{}) << '\n';
        std::cout << "Reverse sorted? " << is_reverse_sorted(vec.begin(), vec.end(), std::less{}) << '\n';
    }
    std::cout << '\n';

    // upper_bound
    {
        std::vector<int> vec = {1, 2, 2, 3, 4, 4, 4, 5, 6, 7, 7, 8, 9, 10, 10};
        auto it_lower = std::lower_bound(vec.begin(), vec.end(), 4, std::less{});
        auto it_upper = my_upper_bound(vec.begin(), vec.end(), 4, std::less{});
        std::cout << "Lower bound position: " << (it_lower - vec.begin()) << '\n';
        std::cout << "Upper bound position: " << (it_upper - vec.begin()) << '\n';
    }
    std::cout << '\n';

    // longest subsequences
    {
        std::vector<int> vec = { 1, 10, 2, 9, 2, 8, 8, 3, 7, 4, 5, 6, 6, 7, 5, 5, 8, 4, 9, 3, 9, 2, 10, 1 };
        auto lis = longest_increasing_subsequence(vec.begin(), vec.end(), std::less{});
        std::cout << "LIS: ";
        for (int value: lis) {
            std::cout << value << ' ';
        }
        std::cout << '\n';
        auto lds = longest_decreasing_subsequence(vec.begin(), vec.end(), std::less{});
        std::cout << "LDS: ";
        for (int value: lds) {
            std::cout << value << ' ';
        }
        std::cout << '\n';
        auto lnds = longest_non_decreasing_subsequence(vec.begin(), vec.end(), std::less{});
        std::cout << "LNDS: ";
        for (int value: lnds) {
            std::cout << value << ' ';
        }
        std::cout << '\n';
        auto lnis = longest_non_increasing_subsequence(vec.begin(), vec.end(), std::less{});
        std::cout << "LNIS: ";
        for (int value: lnis) {
            std::cout << value << ' ';
        }
        std::cout << '\n';
    }
    std::cout << '\n';

    // Folds
    {
        using namespace std::string_literals;

        std::vector<std::string> vec = { "iteration ", "from ", "left ", "is ", "what ", "is ", "right ", "with ", "ranges " };

        std::cout << "Original: " << std::ranges::fold_left(vec, ""s, std::plus{}) << '\n';
        std::cout << "Reversed: " << std::ranges::fold_left(vec | std::views::reverse, ""s, std::plus{}) << '\n';
        std::cout << "std::flip: " << std::ranges::fold_left(vec, ""s, std::flip(std::plus{})) << '\n';
    }
    std::cout << '\n';

    // Fold right from fold left
    {
        std::vector<int> vec = { 1, 10, 2, 9, 2, 8, 8, 3, 7, 4, 5, 6, 6, 7, 5, 5, 8, 4, 9, 3, 9, 2, 10, 1 };
        std::cout << "std::ranges::fold_right: " << std::ranges::fold_right(vec, 0, std::minus{}) << '\n';
        std::cout << "Custom fold_right: " << do_fold_right(vec, 0, std::minus{}) << '\n';
    }
}
