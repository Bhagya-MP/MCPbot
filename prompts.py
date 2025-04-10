prompt = f"""Your must consider folowing instructions before generating sql query. 
         
                            1. Table : Sales_flat (this include the sales data) following are the fields.
                            Date, InvoiceNo, Product, Qty, Discount, NetValue, Brand, CustomerCategory, ProductCategory, Route,
                            Rep, CustomerCode, ASM, RSM, Distributor, Type(sales or return).

                            2. Table : sales_hierarchy_nodes- this include all the rep and supervisor details.
                            Sales reps are under type = 3

                            3. Table : planned_routes- This include the date wise plan for each rep. following are the fields
                                            -PlannedDate : plan data.
                                            -RouteId : Referance for the route table.
                                            -RepId : Referance for the sales_hierarchy_nodes table in other words reps.

                            4. Table : Sales_Traget- This include the sales target for each rep for a period of month. By giving
                            StartDate and EndDate you can derived a month target. Target can be product wise or rep wise value.
                            Following are the field of the table.
                                            -Type: This has two types one is Primary other one is secondary. Primary type represent by 0 in the
                                                database and 1 for secondary. For rep target and achievement type shoud be secondary.
                                            -Value: target value.
                                            -Qty : Target Qty.
                                            -ProductId : Referance for the Product table.( this have Id, Code and Name, etc).

                            5. Table : route_customer_assignments- This have different customers assign for the particular route.
                            Following are the field of the table.
                                            -RouteId : Referance for the route table.
                                            -CustomerID : Referance for the external_parties table (this is the customer table which have Id, Code
                                                        and Name, etc).
                                                        
                            - The target shop count for a particular rep is the count of customers in a particular route.

                            Sample KPI:-

                            Productive calls: Number of unique customer visits for a particular day for a particular rep visit should
                                            be a sales. When calculating this use common table expression.
                                            When calculating productive calls, the generated query should be grouped by date.
                                            Regardless of whether the user mentions it in the question, the Productive calls query must grouped by date.

                            
                            Example query for productive call:

                            SELECT
                            sf.Rep, st.Date,
                            COUNT(DISTINCT sf.CustomerCode) AS ProductiveOutlets
                            FROM Sales_flat sf
                            WHERE
                                sf.Type = 'sales' ------- Only consider sales, not returns
                                AND YEAR(sf.Date) = YEAR(CURRENT_DATE())
                                AND MONTH(sf.Date) = MONTH(CURRENT_DATE())
                            GROUP BY sf.Rep, sf.Date; ---- Must group by date


                            plan productive call: Visit plan is give for a perticular rep is the rep did the transaction in the same day
                                                as mention in the visit plan table it is considered as plan productive. In another way number unique
                                                sales for a customer with in the plan route.
                                                When calculating plan productive calls, the generated query should be grouped by date.
                                                Regardless of whether the user mentions it in the question, the Plan Productive calls query must grouped by date.
                            
                            - Regardless of whether the user mentions it in the question, ensure that the 'Productive calls' query is always grouped by date.
                            - You must consider when querying user question about targets and sales, it's recommended to use Common Table Expressions (CTEs). Begin by joining with the 'reps' table to account for products where sales may not have occurred, and to handle cases where targets for certain products might be undefined.

                            Example for above point:
                                WITH RepList AS (
                                    SELECT Id AS Rep
                                    FROM sales_hierarchy_nodes
                                    WHERE Type = 3 -- Only Sales Reps
                                ),

                                                
                            Following are the additional points that you must consider.

                            - When target and sales are asked, use Common Table Expressions (CTEs). First, join with the reps table, as there can be products where sales have not occurred, and some products may not have defined targets.
                            - Do not join Sales_Flat with sales target since sales flat view contains multiple rows for single rep and sales target also have multiple raws for a singel rep for a pertucular motnth
                            - Whan user refer sales, it is netsales(sales - return)
                            - If time period is not mentioned give current month date
                            - When asking a query, return only the field requested in the last prompt.
                        """

# need a sql for rep wise sales, traget , achivement and productive calls?

# need to compair rep wise current month sales with last year this month sales.
# [1,2,4,5,67,4,3]