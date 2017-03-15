
--
-- Database: `osm_contributions`
--

-- --------------------------------------------------------

--
-- Table structure for table `contributions`
--

CREATE TABLE `contributions` (
  `id` int(11) NOT NULL,
  `username` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_year` int(11) NOT NULL,
  `created_month` int(11) NOT NULL,
  `created_day` int(11) NOT NULL,
  `changeset_id` int(11) NOT NULL,
  `building_created` int(11) NOT NULL,
  `building_modified` int(11) NOT NULL,
  `building_deleted` int(11) NOT NULL,
  `node_created` int(11) NOT NULL,
  `node_modified` int(11) NOT NULL,
  `node_deleted` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Indexes for table `contributions`
--
ALTER TABLE `contributions`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contributions`
--
ALTER TABLE `contributions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=744;
