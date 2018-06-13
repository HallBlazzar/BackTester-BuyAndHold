# This is Buy And Hold Strategy developed by BackTester Framework #

## Requirement ##

* [python3](https://www.python.org/) (>3.6)
* [pandas](https://pandas.pydata.org/) (> v0.23.0)
* [numpy](http://www.numpy.org/) (> v1.14)
* [dateutl](http://dateutil.readthedocs.io/en/stable/) (>2.7.0)

## Usage ##

1. Set parameters

   In `Main.py`:

   1. Prepare data for framework

      ```python
      back_test_context = BackTesterContext(
          price_information_generator=PriceInformationGenerator(data_source).generate_price_information(
              start_date=datetime.strptime('1998/07/21', '%Y/%m/%d'),
              end_date=datetime.strptime('2016/12/30', '%Y/%m/%d')
          ),
          trading_status_calculator=TradingStatusCalculator(success_rate=100)
      )
      ```
       Data format ( in `pandas.DataFrame `) required by framework is shown below:

       | Column Name | Data Type |
       |-----------------|-------------|
       | date | datetime64[ns] |
       | contract | str/object |
       | delivery_month | str/object |
       | open_price | float64 |
       | highest_price | float64 |
       | lowest_price | float64 |
       | close_price | float64 |

       You can add arbitrary columns if you need, but columns and their data type above are immutable when passing `DataFrame` to `PriceInformationGenerator`:

   2. Configure time interval and success rate of order

      ```python
      back_test_context = BackTesterContext(
              price_information_generator=PriceInformationGenerator(data_source).generate_price_information(
                  start_date=datetime.strptime('1998/07/21', '%Y/%m/%d'),
                  end_date=datetime.strptime('2016/12/30', '%Y/%m/%d')
              ),
              trading_status_calculator=TradingStatusCalculator(success_rate=100)
      )
      ```

       1. `BackTesterContext` will iterate from  `start_date` to `end_date`. During iterating progress, if any date in `DataFrame` you passed exist, all rows with same date will be read.

       2. When `success_rate` to `BackTesterContext`, you can set success rate when `BackTesterContext` filling orders. When you passing orders to `BackTesterContext`, if success_rate is less than 100, then every order will have chance to be fail traded.

   3. Configure initial capital

      ```python
      asset_maintainer = AssetMaintainer(
          initial_capital=1000000, price_parameter=pd.read_csv(os.path.join('Source', 'price_parameter.csv'))
      )
      ```

   4. Configure your target contract

      ```python
      buy_and_hold = BuyAndHold(
            asset_maintainer=asset_maintainer, back_test_context=back_test_context, target_contract='TX'
      )
      ```

2. Run `Main.py`

## Note ##

1. When developing strategy, you can access

   * `AssetMaintainer.current_position_status_maintainer.current_position_status` (`pandas.DataFrame`)

     | Column Name | Data Type |
     |-----------------|-------------|
     | contract | str/object |
     | delivery_month | str/object
     | value | float64 |
     | cost | float64 |
     | close_price_of_prefious_trading_date | float64 |
     | status | str/object |

     * `status` always = `'holding'`
     * Buying time of contracts with same `contract` and `delivery_month` can be specified through their sequence of index. Smaller means bought earlier. When selling, contracts with smaller index number will be sold first.

   * `AssetMaintainer.current_capital_maintainer.current_capital` (`int`)

   to get `current_position_status` and `current_capital`.

2. When sending order in strategy through `BackTesterContext.send_order`, you have to follow the format:

    * data_type: `pandas.DataFrame`

    * format:

      | Column Name | Data Type |
      |-----------------|-------------|
      | contract | str/object |
      | delivery_month | str/object |
      | buy_position | int |
      | sell_position | int |
